name: James Taylor
sid: 592115506

This is an updated version. See what is new in next section.

The main.py script requires one argument, the file from which to read the data. On sensible operating systems (Linux, BSD, MacOSX) you can just run:

    ./main.py data.txt

If execute permission is not set properly, or your python3 is not installed in the default location, or you have a bad operating system (Windows) then you may instead need to run:

    python3 main.py data.txt

In addition to the full data in data.txt I have provided some test files to demonstrate the new features.

_______________ New in this version ________________

The program will accept data with as little as one single value, and it can accept any number of rows and columnms limited only by available memory.

The rows of data can be of different lengths, but there must be a value in each column leading up to the last value on each row because this is how we know which month column it is.

Some or all of the data values may be "outliers", ie. outside of the range defined as valid by the constants set at the top of the program. Outliers are excluded from all calculations of statistics (average, minimum, and maximum) for both cities and seasons.

The presence of outliers does not disturb the column alignment used to extract the seasons.

Seasons do not have to contain complete data. If there is only enough data for part of a season then we can still report the average, min, and max.

If there is a city or a season with no good data (all outliers) then instead of printing statistics the program will report --- no good data --- for that city or season.

If there were any outliers the program will report how many it found.

The Python source is commented with more explanation.

# to run all the tests on a "real" computer type:
bash$ for file in data.txt test*; do echo $'\n'"========== $file =========="; ./main.py "$file"; done

_______________ Output ________________


========== data.txt ==========

City average, min, and max:
City  1: avg  9.08, min -2, max 21
City  2: avg 24.17, min 20, max 28
City  3: avg 12.92, min -1, max 26
City  4: avg 19.92, min 11, max 27
City  5: avg  7.67, min -8, max 22
City  6: avg 19.92, min 10, max 28
City  7: avg 22.17, min 12, max 33
City  8: avg 11.25, min  5, max 18
City  9: avg 13.75, min 10, max 17
City 10: avg 17.25, min 13, max 22

Season average, min, and max:
Season 1: avg  8.90, min -8, max 22
Season 2: avg 18.73, min  7, max 31
Season 3: avg 23.03, min 15, max 33
Season 4: avg 12.57, min -5, max 26

Season avg extremes:
Min avg is season 1
Max avg is season 3

Seasons in decending order of avgerage:
Season 3 > Season 2 > Season 4 > Season 1


========== test1.txt ==========

City average, min, and max:
City  1: avg  9.08, min -2, max 21
City  2: avg 24.17, min 20, max 28
City  3: avg 11.73, min -1, max 25
City  4: avg 19.92, min 11, max 27
City  5: avg  7.73, min -8, max 22
City  6: avg 20.82, min 12, max 28
City  7: avg 22.17, min 12, max 33
City  8: avg 10.64, min  5, max 18
City  9: avg 13.75, min 10, max 17
City 10: avg 17.09, min 13, max 22

Season average, min, and max:
Season 1: avg  8.86, min -8, max 22
Season 2: avg 19.14, min  8, max 31
Season 3: avg 23.11, min 15, max 33
Season 4: avg 12.34, min -5, max 26

Season avg extremes:
Min avg is season 1
Max avg is season 3

Seasons in decending order of avgerage:
Season 3 > Season 2 > Season 4 > Season 1

There were 5 outliers


========== test2.txt ==========

City average, min, and max:
City  1: avg  9.08, min -2, max 21
City  2: avg 24.17, min 20, max 28
City  3: avg 12.92, min -1, max 26
City  4: --- no good data ---
City  5: avg  7.67, min -8, max 22
City  6: avg 19.92, min 10, max 28
City  7: avg 22.17, min 12, max 33
City  8: avg 11.25, min  5, max 18
City  9: avg 13.75, min 10, max 17
City 10: avg 17.25, min 13, max 22

Season average, min, and max:
Season 1: avg  8.41, min -8, max 22
Season 2: avg 18.22, min  7, max 31
Season 3: avg 22.63, min 15, max 33
Season 4: avg 12.15, min -5, max 26

Season avg extremes:
Min avg is season 1
Max avg is season 3

Seasons in decending order of avgerage:
Season 3 > Season 2 > Season 4 > Season 1

There were 12 outliers


========== test3.txt ==========

City average, min, and max:
City  1: avg  7.56, min -2, max 21
City  2: avg 23.78, min 20, max 28
City  3: avg 11.22, min -1, max 26
City  4: avg 18.78, min 11, max 27
City  5: avg  5.78, min -8, max 22
City  6: avg 18.78, min 10, max 28
City  7: avg 20.89, min 12, max 33
City  8: avg 10.67, min  5, max 18
City  9: avg 13.67, min 10, max 17
City 10: avg 17.22, min 13, max 22

Season average, min, and max:
Season 1: avg  8.90, min -8, max 22
Season 2: --- no good data ---
Season 3: avg 23.03, min 15, max 33
Season 4: avg 12.57, min -5, max 26

Season avg extremes:
Min avg is season 1
Max avg is season 3

Seasons in decending order of avgerage:
Season 3 > Season 4 > Season 1

There were 30 outliers


========== test4.txt ==========

City average, min, and max:
City  1: avg  9.17, min -2, max 21
City  2: avg 24.17, min 20, max 28
City  3: avg 13.00, min -1, max 26
City  4: --- no good data ---
City  5: avg  7.50, min -8, max 22
City  6: avg 20.00, min 10, max 28
City  7: avg 22.83, min 12, max 33
City  8: avg 11.67, min  5, max 18
City  9: --- no good data ---
City 10: avg 17.67, min 13, max 22

Season average, min, and max:
Season 1: avg  8.04, min -8, max 22
Season 2: --- no good data ---
Season 3: avg 23.46, min 16, max 33
Season 4: --- no good data ---

Season avg extremes:
Min avg is season 1
Max avg is season 3

Seasons in decending order of avgerage:
Season 3 > Season 1

There were 72 outliers


========== test5.txt ==========
No good valid data found in file test5.txt
