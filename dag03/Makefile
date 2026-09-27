TEXFILES = $(wildcard *.tex)
SLIDES   = $(notdir $(firstword $(TEXFILES)))
BASENAME = $(basename $(SLIDES))

.PHONY: handout slides clean

handout:
	pdflatex -jobname=$(BASENAME)_handouts "\def\handoutmode{1}\input{$(SLIDES)}"

slides:
	pdflatex -jobname=$(BASENAME) "$(SLIDES)"

clean:
	del /Q $(BASENAME)*.aux $(BASENAME)*.log $(BASENAME)*.nav $(BASENAME)*.out $(BASENAME)*.snm $(BASENAME)*.toc $(BASENAME)*.vrb 2>NUL || exit 0
