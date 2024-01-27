#!/bin/bash

pandoc output.md -o output.tex --standalone
pdflatex -interaction=nonstopmode -pdf output.tex
