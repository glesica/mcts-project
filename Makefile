PDFNAMES=slides.pdf paper.pdf

all: build clean

clean:
	-rm -f *.aux
	-rm -f *.log
	-rm -f *.bbl
	-rm -f *.blg
	-rm -f *.out

build: $(PDFNAMES)

%.pdf: %.tex
	pdflatex $<
	#bibtex $*
	pdflatex $<
	#pdflatex $<

slides.pdf: slides.markdown
	pandoc -t beamer -V theme:Rochester $< -o $@

paper.pdf: paper.markdown
	pandoc --bibliography citations.bib --csl ~/ieee.csl $< -o $@
