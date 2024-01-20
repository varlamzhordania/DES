import subprocess, os

from django.conf import settings
from django.http import Http404

from .models import Theme

css_folder = os.path.join(settings.STATICFILES_DIRS[0], "assets", "css")
styles_file = os.path.join(css_folder, "theme.scss")


def update_theme(obj):
    with open(styles_file, 'w'):
        pass

    update_theme_file(obj)
    compile_scss_to_css(obj)


def update_theme_file(obj):
    try:
        theme = obj
        content = f"""
$primary: {theme.primary_color};
$secondary: {theme.secondary_color};
$success: {theme.success_color};
$info: {theme.info_color};
$warning: {theme.warning_color};
$danger: {theme.danger_color};
$light: {theme.light_color};
$dark: {theme.dark_color};

$body-bg: {theme.body_bg_color};
$text-color: $dark;
$link-color: $primary;
$link-hover-color: darken($primary, 10%);

$border-radius: 0.7rem;
$input-border-radius: 0.5rem;

@import "../../../bootstrap-5.3.2/scss/bootstrap";

.form-control {{
  border-width: 2px;
  background-color: $gray-200;
}}

.form-control:focus {{
  outline: none;
  border-color: rgba($dark, 1);
  box-shadow: none;
  background-color: $gray-200;
}}
        """

        # Write the content to theme.scss
        with open(os.path.join(css_folder, "theme.scss"), 'w') as f:
            f.write(content)
    except Theme.DoesNotExist:
        raise Http404("Theme does not exist")


def compile_scss_to_css(obj):
    input_file = styles_file
    output_file = os.path.join(css_folder, f"{obj.id}-theme.css")
    subprocess.run(['sass', str(input_file), str(output_file)], check=True, shell=True)
