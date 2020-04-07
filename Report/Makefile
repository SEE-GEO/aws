aws_325ghz_study.pdf: aws_325ghz_study.tex Makefile *.tex *.bib
	pdflatex $(@:%.pdf=%)
	bibtex $(@:%.pdf=%)
	pdflatex $(@:%.pdf=%)
	pdflatex $(@:%.pdf=%)
	pdflatex $(@:%.pdf=%)
	rm -f *.log *.blg *.bbl *.aux *.dvi *.out *.toc

clean:
	rm -f *.log *.blg *.bbl *.aux *.dvi *.out *.toc

clean-all: clean
	rm -f aws_325ghz_study.pdf

