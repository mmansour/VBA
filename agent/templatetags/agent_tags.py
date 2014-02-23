
from __future__ import with_statement
import os
from urllib import urlopen, urlencode, quote, unquote
from django.core.files import File
from django.core.files.storage import default_storage
from PIL import Image, ImageFile, ImageOps
from mezzanine.conf import settings
from mezzanine import template

register = template.Library()

@register.simple_tag
def agent_thumbnail(image_url, width, height, quality=95):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image. if width or height are zero then original ratio is
    maintained.
    """
    if not image_url:
        return ""

    image_url = unquote(unicode(image_url))
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")
    thumb_name = "%s-%sx%s%s" % (image_prefix, width, height, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir,
                             settings.THUMBNAILS_DIR_NAME)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = "%s/%s" % (settings.THUMBNAILS_DIR_NAME,
                           quote(thumb_name.encode("utf-8")))
    image_url_path = os.path.dirname(image_url)
    if image_url_path:
        thumb_url = "%s/%s" % (image_url_path, thumb_url)

    try:
        thumb_exists = os.path.exists(thumb_path)
    except UnicodeEncodeError:
        # The image that was saved to a filesystem with utf-8 support,
        # but somehow the locale has changed and the filesystem does not
        # support utf-8.
        from mezzanine.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()
    if thumb_exists:
        # Thumbnail exists, don't generate it.
        return thumb_url
    elif not default_storage.exists(image_url):
        # Requested image does not exist, just return its URL.
        return image_url

    image = Image.open(default_storage.open(image_url))
    image_info = image.info
    width = int(width)
    height = int(height)

    # If already right size, don't do anything.
    if width == image.size[0] and height == image.size[1]:
        return image_url
    # Set dimensions.
    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    if image.mode not in ("L", "RGBA"):
        image = image.convert("RGBA")
    # Required for progressive jpgs.
    ImageFile.MAXBLOCK = image.size[0] * image.size[1]
    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS, centering=(0, 0, 0, 0))
        image = image.save(thumb_path, filetype, quality=quality, **image_info)
        # Push a remote copy of the thumbnail if MEDIA_URL is
        # absolute.
        if "://" in settings.MEDIA_URL:
            with open(thumb_path, "r") as f:
                default_storage.save(thumb_url, File(f))
    except Exception:
        # If an error occurred, a corrupted image may have been saved,
        # so remove it, otherwise the check for it existing will just
        # return the corrupted image next time it's requested.
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return image_url
    return thumb_url