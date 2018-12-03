##
#
#  Makefile for Website
#
#  https://bitbucket.org/fret/website.git
#
# Copyright 2018 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###

BUILD = $$(pwd)/build
DIST = $$(pwd)/dist
SRC = $$(pwd)/src
HTML = $(SRC)/pages
JS = $(SRC)/js
JS_DIST = $(DIST)/js
CSS = $(SRC)/css
CSS_BUILD = $(BUILD)/css
CSS_DIST = $(DIST)/css
NODE = $$(pwd)/node_modules
BOOTSTRAP_SCSS = $(NODE)/bootstrap/scss
BOOTSTRAP_JS = $(NODE)/bootstrap/dist/js/bootstrap.min.js
JQUERY_JS = $(NODE)/jquery/dist/jquery.min.js
ESLINT = $(NODE)/eslint/bin/eslint.js


include website.mk
