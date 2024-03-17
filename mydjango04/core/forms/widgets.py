import dataclasses
import datetime
from django.conf import settings
from django.forms import RadioSelect, Select, TextInput
from django import forms
from django.forms.widgets import ClearableFileInput
from typing import Callable, Dict, List, Tuple, Union
from django.forms.widgets import MultiWidget
from django.forms.widgets import DateInput


class CounterTextInput(TextInput):
    template_name = "core/forms/widgets/counter_text.html"


class IosSwitchInput(forms.CheckboxInput):
    def __init__(self, attrs=None, check_test=None):
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " ios-form-switch"
        super().__init__(attrs, check_test)

    class Media:
        # 의존성 있는 css/js 파일 경로를 지정
        # 템플릿에서는 {{ form.media }}를 통해 중복을 제거한 script/link 자동 생성
        css = {
            "all": [
                "core/forms/widgets/ios_form_switch.css",
            ],
        }


class PreviewClearableFileInput(ClearableFileInput):
    template_name = "core/forms/widgets/preview_clearable_file.html"


class HorizontalRadioSelect(RadioSelect):
    template_name = "core/forms/widgets/horizontal_radio.html"


class StarRatingSelect(Select):
    template_name = "core/forms/widgets/star_rating_select.html"

    class Media:
        css = {
            "all": [
                "core/star-rating-js/4.3.0/star-rating.min.css",
            ]
        }
        js = ["core/star-rating-js/4.3.0/star-rating.min.js"]


# 3개의 TextInput를 서브 위젯로 둘 것이기에, MultiWidget을 상속받습니다.
class PhoneNumberInput(MultiWidget):
    subwidget_default_attrs = {
        "style": "width: 6ch; margin-right: 1ch;",
        "autocomplete": "off",
    }

    def __init__(self, attrs=None):
        # 서브 위젯을 리스트로 부모 생성자로 넘깁니다.
        widgets = [
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"01\d",
                    "maxlength": 3,
                }
            ),
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"\d{4}",
                    "maxlength": 4,
                }
            ),
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"\d{4}",
                    "maxlength": 4,
                }
            ),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value: str) -> Tuple[str, str, str]:
        """각 서브 위젯에 값을 반영할 때, 호출됩니다."""
        if value:
            # 구분자는 제거하고, 순서대로 3자리/4자리/4자리 문자열을 뽑습니다.
            value = re.sub(r"[ -]", "", value)
            return value[:3], value[3:7], value[7:]
        return "", "", ""

    def value_from_datadict(self, data, files, name) -> str:
        """서브 위젯의 값들을 하나의 문자열로 합쳐서 반환. 위젯은 유효성 검사의 책임이 없습니다."""
        values = super().value_from_datadict(data, files, name)
        return "".join(values)


class DatePickerInput(DateInput):
    template_name = "core/forms/widgets/date_picker.html"

    class Media:
        css = {
            "all": [
                "core/vanillajs-datepicker/1.3.4/css/datepicker-bs5.min.css",
            ]
        }
        js = ["core/vanillajs-datepicker/1.3.4/js/datepicker.min.js"]


class NaverMapPointInput(TextInput):
    template_name = "core/forms/widgets/naver_map_point.html"

    def __init__(self, zoom=10, scale_control=True, zoom_control=True, attrs=None):
        self.zoom = zoom
        self.scale_control = scale_control
        self.zoom_control = zoom_control
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["naver_map_options"] = {
            "zoom": self.zoom,
            "scaleControl": self.scale_control,
            "zoomControl": self.zoom_control,
        }
        return context

    class Media:
        js = [
            "https://openapi.map.naver.com/openapi/v3/maps.js?ncpClientId="
            + settings.NAVER_MAP_POINT_WIDGET_CLIENT_ID,
        ]
