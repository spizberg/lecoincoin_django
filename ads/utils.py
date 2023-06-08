from .models import Illustration
import uuid
from pathlib import Path
from django.conf import settings
from typing import Union, List


illustration_images_path = 'ads/static/ads/images/illustrations'


def create_illustrations(salead_files: list) -> Union[Illustration, None]:
    """
    Create single or multiple illustrations by using uploaded images

    @param salead_files:
    @return:
    """
    illustrations = []
    for salead_file in salead_files:
        filename = f'{str(uuid.uuid4())}.{salead_file._get_name().split(".")[-1]}'
        new_file = Path(settings.BASE_DIR, illustration_images_path, filename)
        with open(str(new_file), 'wb+') as illustration_file:
            for chunk in salead_file.chunks():
                illustration_file.write(chunk)
        illustration = Illustration(filename=filename)
        if not isinstance(illustration, Illustration):
            return None
        illustrations.append(illustration)
    return illustrations


def delete_illustrations(illustrations: List[Illustration]) -> None:
    for illustration in illustrations:
        Path(illustration_images_path, illustration.filename).unlink(missing_ok=True)
        illustration.delete()
