Technical Notes
===============

Why quick select feature was removed from python search select (PSS)?

Quick select needed to assign a unique key (0-9, a-z) to each item. Using
unique key you can provide 36 quick select which was nice, but then since the
characters were used a quick select, some differentiation was needed to find if
a character key was pressed to support quick select or to perform a search. To
make support such a distinction, two modes - command and insert were added to
the PSS. But after the addition of the modes, things becomes ugly and no so
simple, so I have removed it.
