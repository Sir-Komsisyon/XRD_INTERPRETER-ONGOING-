# XRD_INTERPRETER-ONGOING-
This is an ongoing project, please feel free to recommend

I'm building a an XRD intepreter that can analyze data from known sources, from that I've already built scraper that can scrape data, howver it is till in devlopment

So the data base is the most important for this:


PSUEDOCODE:

1. PDF (w/XRD result) gets analyzed for peaks (INIATE SET LIMIT FOR theta and RELATIVE VALUES BASED On machine SETted values_
2. Python gets data for a. Relative Intensity b. 2Theta c. d-spacing
3. If peaks are scattered, get (isolate) parts with many peaks
4. Convert peaks into table
5. Use Bragg's Law equation to get values arranged in columns (PEAK | 2theta | Relative Intensity | d-spacing | Theta )
6. Graph the values in the column
---- DATABASE 
7.From Database Arranged in Similar column ((PEAK | 2theta | Relative Intensity | d-spacing | Theta )) (Scraped from Outside Sources) Get Library with similar values of the calculated columns
8. SET confidence limit for each column value
9. If SET confidence within standards of the calculated values , PRINT %Confidence
10. GRAPH result with highest confidecne and print Graph
11. LET user compare it with, if not user satisfied
12. GRAPH 2nd result with highest confidence and LET use compare, continue until satisfied
13. 
