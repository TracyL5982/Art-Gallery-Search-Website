[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/W1s0QYwu)
# Pset 3: Web Application (Version 1)

### Due Friday Nov 3 11:59 PM NHT (New Haven Time)

## Table of Contents
- [Pset 3: Web Application (Version 1)](#pset-3-web-application-version-1)
    - [Due Friday Nov 3 11:59 PM NHT (New Haven Time)](#due-friday-nov-3-1159-pm-nht-new-haven-time)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Rules](#rules)
  - [Getting Started](#getting-started)
  - [Your Task](#your-task)
  - [The Database](#the-database)
  - [The Application](#the-application)
  - [Additional Requirements for 519 Students](#additional-requirements-for-519-students)
    - [Required Additional Feature](#required-additional-feature)
    - [Optional Additional Features](#optional-additional-features)
  - [Specific Endpoints](#specific-endpoints)
  - [Error Handling: Bad Server](#error-handling-bad-server)
  - [Error Handling: Bad Client](#error-handling-bad-client)
    - [Invalid search parameters](#invalid-search-parameters)
    - [Invalid `obj_id`](#invalid-obj_id)
    - [Missing `obj_id`](#missing-obj_id)
    - [Aside: Error Pages](#aside-error-pages)
    - [Other invalid requests](#other-invalid-requests)
  - [Source Code Guide](#source-code-guide)
  - [Submission](#submission)
    - [Late Submissions](#late-submissions)
    - [Grading](#grading)

## Purpose

The purpose of this assignment is to help you learn or review web programming in Flask, including HTML.

---

## Rules

You may work with one teammate on this assignment, and we prefer that you do so.

It must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
Your `README` file and your source code files must contain your name and your teammate’s name.

---

## Getting Started
> **Note**: this section contains exactly the text on the Canvas assignment, reproduced here only for completeness of this document.
> Since you made it here, you can safely ignore this section.

1. Accept [this GitHub classroom assignment](https://classroom.github.com/a/x4M2JGGT).
   * Select your team.
     * This step creates a GitHub repository for your team and links your team members' GitHub ids.
   * If you do not have a GitHub account, you are required to create one for this course
   * Use this git repository to track your assignment development.

2. Download the `lux.sqlite` database file from Canvas (or copy it over from your previous assignment) and place it in your new repository folder.
  > **Important**: Do not track `lux.sqlite` in your git repository.
  > It is too large to be hosted on GitHub and recovering from an error telling you that is challenging at best.
  > The included `.gitignore` file in the template repository will help with this, so *do not change or remove* that file.
  > You may keep the database file in the repository folder, but you must be careful not to *track* it.

---

## Your Task

As with Psets 1 and 2, assume you are working for the Yale University Art Galleries (YUAG).
You are given a database containing data about objects and artwork stored in the gallery's collection.
Your task is to compose an application that allows museum visitors and other interested parties to query the database.

---

## The Database

The database is identical to the one from Psets 1 and 2.
Refer to the Pset 1 specification for the list of tables and fields in the database.
As with previous psets, the database is in a file named `lux.sqlite` that you should copy into your repository but take care not to track with git.

---
## The Application

Compose a program named `runserver.py`.
When executed with `-h` as a command-line argument, the program must display the following help message describing the program's behavior:

```
$ python runserver.py -h
usage: runserver.py [-h] port

The YUAG search application

positional arguments:
  port        the port at which the server should listen

optional arguments:
  -h, --help  show this help message and exit
```

> **Note**: The specific verbiage of this help message should be the default for your version of the `argparse` module, which differs slightly between python versions.

Your `runserver.py` must run an instance of the Flask test server on the specified port, which must in turn run your application.

> **Note**: Your application code should *not* be in your `runserver.py` program, which should do nothing but start a Flask server on the provided port number.
> The file containing your application code may be named whatever you want, but we suggest something simple such as `luxapp.py`.

When a client makes an HTTP request to the server, your application must return an HTML webpage appropriate to the request.
Beyond some [specific endpoints](#specific-endpoints) mentioned below, there are several requirements your application must satisfy:
* Your application's **primary web page** (*i.e.*, the webpage returned by a request to the server's root&mdash;*e.g.* `http://yourserver:80/` if your server is listening on port 80) must contain an **HTML form**.
  * The form must include four text input fields labeled "Label", "Classifier", "Agent" and "Department".
    These should, respectively, allow the user to specify an object label, a classifier, the name of an agent, and a YUAG department.
  * In addition to the text input fields, your form must include a `submit` input field.
  For this assignment, the submit field must be a button labeled "Search".
  * The form may contain other input elements, but any additional elements you include in the form must be of the `hidden` type (that is, they must not be visible to the user when they view the webpage).
  * The form input fields must be filled in with the parameters used to make the most recent query, that is, the values of the input fields as they were upon the most recent submission of the form (if the form has never been submitted, those fields should be empty)
* After submission the form, the webpage must display an HTML `table` containing no more than the first 1000 results of the query that was triggered by the most recent submission of the form (or nothing at all if the form has not yet been submitted).
  * If the user entered no text in the form elements, the webpage should display a message such as "No search terms provided. Please enter some search terms."
    > **Note**: This is a change in requirements from previous psets, in which an empty search returned all objects in the database.
  * The columns displayed in the table must be&mdash;in order&mdash;the object's label, the object's date, the name of each agent that produced this object and the part they produced (in the format `"{agent-name} ({agent-part})"`), and a list of all classifiers for the object, for each object that matches the specified criteria, or of all objects in the database if the user specifies no criteria.
  The columns must be labeled "Label", "Date", "Agents", and "Classified As", respectively.
    * The lists of things in the "Agents" and "Classified As" columns must be formatted with one item per line
  * The table rows must be _sorted_; the algorithm to sort is the same from Pset 2.
  * A user must be able to click on the `label` for any of the displayed objects to request more information about that object on a different webpage (the "secondary" page) at the url `"/obj/{object-id}"`.
    The requirements for the secondary webpage are below.
    > **Note**: The object's ID must not be displayed in the table!
* You application must accept requests to the endpoint `/obj/<int:obj_id>` (where `obj_id` is the ID of the clicked-on object).
The webpage returned at this endpoint must satisfy the following requirements:
  * It must display at least the following information about the selected object:
    * A section with header "Summary" containing the following pieces of information in a single-row **HTML table**:
      * The object's accession number, labeled "Accession no."
      * The object's date, labeled "Date"
      * The object's place, labeled "Place"
    * A section with header "Label" containing the object's label
    * A section with header "Produced By", containing an **HTML table** with details of all agents that produced this object.
    The table must have the following column headers and content:
      * "Part", containing the part of the production carried out by each agent
      * "Name", containing the name of each agent
      * "Nationalities", containing all nationalities of each agent, each on its own line
      * "Timespan", containing the *year* of each agent's `begin_date` and the *year* of each agent's `end_date`, separated by a dash or hyphen
        * Some agents are still alive/active; in those cases the Timespan column must contain text such as "1967&ndash;"
        * An agent that has no timespan should have that fact displayed in this column in some reasonable manner
        > **Note**: The table in the "Produced By" section must be sorted in ascending order of agent name, then part, then timespan and finally by nationality.
    * A section with header "Image", containing an image of the object
      * Some objects do not have images. For those objects, this section must *not* be present in the rendered webpage
      * For objects that *do* have images, you should display the image stored at a URL with the pattern:
        ```
        https://media.collections.yale.edu/thumbnail/yuag/obj/{obj-id}
        ```
    * A section with header "Classified As", containing an **unordered list** of all classifiers for the object, sorted in ascending order of the classifier name
      > **Note**: Despite the name "unordered list" given to the HTML `<ul>` element, the list in this case must be sorted in a particular order.
      > In HTML, an unordered list is simply a list in which the items are not numbered.
    * A section with header "Information", containing an **unordered list** of all `references` to the object, with each item in the following format.
      ```html
      <li><strong>{{ reference.type }}:</strong> {{ reference.content }}</li>
      ```
      The list must be sorted first by reference type and then by content.
      > **Note**: Some references contain HTML code verbatim. That HTML must be rendered according to the included elements!

  * Its information must be well-formatted (_e.g._, the headers must be within semantic HTML `<h`*`N`*`>` header elements, and the lists must be within HTML `<ul>` elements)
  * It must provide a link back to the primary webpage to allow the user to perform another search.
  The resulting instance of the primary webpage must contain exactly the same content as was most recently displayed on the page before the user clicked the label of an object to retrieve the secondary webpage, including both the results table and filled-in input fields.

    > **Note**: Your application must be *stateful* to accomplish this.
    > Review the lecture slides and demo code on how to create a stateful web application using cookies.

---
## Additional Requirements for 519 Students

If you *or your partner* are enrolled in CPSC 519, your application must satisfy all of the above requirements and you must implement some of the following features.

If at least one member of your team is enrolled in CPSC 519, you are required to implement label-editing functionality (the [Required Additional Feature](#required-additional-feature)).
If both members of your team are enrolled in CPSC 519, you are *also* required to implement at least one of the [Optional Additional Features](#optional-additional-features-implement-at-least-one).

Even if you and your partner are in 419 and not 519, you are more than welcome to attempt these activities.
They will not have any bearing on your grade for this assignment, but they will provide valuable experience in adding features to a webpage that may prove useful in developing your final project.

### Required Additional Feature

If you *or your partner* are enrolled in CPSC 519, you must implement the following additional feature.

1. On the secondary webpage, add a button or a link labeled "Edit" associated with the "Label" section.
Upon clicking this button, the user must be presented with a webpage containing a form with a `textarea` element (see [this webpage](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/textarea) for details) initially populated with the current value of the label for the object, and a submit button labeled "Submit".
When the user submits this form, it must send an HTTP `POST` request to your server that will change the value of the label for this object in the database to match the new text that the user entered in the text area, and the user should be presented with the secondary webpage showing the object's new label (and, of course, the other required information about the object).
The server must accept this `POST` request at the endpoint `/obj/<int:obj-id>`.

> **Note**: This is the same endpont as the secondary webpage; the only difference is the HTTP method associated with the request: in this case, that method is `POST`; in the other, it is `GET`.

### Optional Additional Features

If you *and your partner* are both enrolled in CPSC 519, you must implement at least one of the following additional features.

2. The default styling of an HTML table is quite ugly in most browsers.
Use CSS to spruce up your tables:
   * Add padding of `5px` to all sides of every cell in each table
   * Add a `1px` wide `gray` border between rows of each table
   * When the mouse hovers over a particular row of each table, change that row's background color to `lightgray`
   * You are free to style your application in any other manner that looks good to you (but nothing else is required)
   * Place your CSS into a file named `styles.css` that is loaded by your primary and secondary webpages, but not included directly in those pages
3. On the primary page, add a button or link labeled "Clear Previous Search" that, when clicked, displays the primary page with empty input fields and no table of results.
It must be the case that clicking the button or link causes any stored state to be reset to an initial or empty state, including any state local to the browser (such as cookies) and any state stored on the server.

---
## Specific Endpoints

There are three endpoints to which your application must respond:
1. `/` must return the primary page
2. `/search?...` must return the results of a search using the parameters in the query string (that is, those that the user entered on the primary page).
   * The parameters accepted by the `/search` endpoint must be `l` (for the label), `a` (for the agent name), `c` (for the classifiers), and `d` (for the date)
3. `/obj/<int:obj_id>` must return the secondary page populated with information about the object with the `id` provided in the query string.

Students completing the [additional 519 activities](#additional-requirements-for-519-students) must add endpoints to accomplish some of those tasks, and the specifics are indicated above.

---
## Error Handling: Bad Server

Since you control the machine that is running both the server application and the database, there is not much we will force you to worry about for server-side errors.
There are, however, two errors that your program must handle gracefully.
1. The server is started with a port that is not a positive integer.
If the server is started with a command such as `$ python runserver.py notaport`, it should display a meaningful error message and exit.
1. The database file does not exist.
If the server attempted to open the `lux.sqlite` file but the file does not exist (or otherwise cannot be opened), your program should display a meaningful error message and exit.

---
## Error Handling: Bad Client

It is an unfortunate truth about web applications of this kind that a user can enter anything they want in their request to your server!
For example, anyone can send a request to a URL such as `http://yourserver:80/obj/gobbeldygook`, despite there being no object with id "gobbeldygook" on which they could have clicked.
This means that starting with this assignment, we will be ramping up the error handling requirements on your software.
Specifically...

### Invalid search parameters

If the user requests a page at a URL such as `http://yourserver:80/search?foo=bar`&mdash;in which the parameters to a search request are not one of `l`, `a`, `c`, or `d`&mdash;your application must treat those parameters as not existing.
For example, in response to a request to the URL `http://yourserver:80/search?foo=bar&a=gogh`, your server must produce a webpage containing results of a search for objects with agent name containing `gogh`.

### Invalid `obj_id`

If the user requests a page at a URL such as `http://yourserver:80/obj/gobbeldygook`&mdash;in which the object ID value does not appear in the database&mdash;the server must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: no object with id gobbeldygook exists". (The "gobbeldygook" part should, of course, be replaced with the actual nonexistent id that was queried.)
This page must be returned with status code 404 (not found).

Your application must respond with this error page for *any* missing crn, including numeric and non-numeric crns.

### Missing `obj_id`

If the user requests a page at a URL such as `http://yourserver:80/obj` (that is, missing a `obj_id`), the application must return an appropriate error page as HTML that displays, at a minimum, text that reads "Error: missing object id." and status code 404 (not found).

### Aside: Error Pages

Your error page must have some required content, but it should not live at a special URL.
That is, your application should behave in a similar manner as Google when an invalid page is requested, such as `google.com/notreal`.
The page displayed should clearly indicate an error occurred, but the URL in the browser should remain `google.com/notreal`: it *should not* be some other URL, such as `google.com/404`.

### Other invalid requests

There are many other requests that the user could send that are "wrong", such as:

* `http://yourserver:notyourport/`
* `http://yourserver:80/notyourapp`
* `http://yourserver:80/search?not/well/formed/url`

The only requirement placed on your server in these cases (and similar ones) is that it does not crash when queried with such requests; that is, if the user sends a valid request immediately after an invalid one, the valid request must get the correct result.

---
## Source Code Guide

Here are the **requirements** for the source code of your solution.

* The `runserver.py` program must start a flask server for your application on the port provided as a command-line argument, listening on all IP addresses
* Your application program must communicate with a SQLite database in a file named `lux.sqlite`, organized as described above.
* Your application program must use SQL prepared statements for every database query.
(This protects the database against SQL injection attacks.)
* Use cookies to keep track of the application's state
* Any display of user-entered content on your webpage must be **escaped** before display. This prevents XSS (cross-site-scripting) attacks

Here are some **recommendations** for the source code of your solution.

* Reuse code from your solution to Pset 2 in this assignment.
* Modularize your application program so that database communication code is cleanly separated from response production code.
    * Use HTML templates to keep your repsonse production code as clear as possible
    * Structure your code according to MVC design principles (the HTML templates are your Views)
* You may use external dependencies, but we advise you not to (with the obvious exception of `flask`).
  This assignment is designed such that everything can be accomplished without too much pain using only packages from the Python standard library.

---
## Submission

Rename this file `TEMPLATE_README.md` and replace it with a new `README.md` file.
Your new `README` file must contain:

* Your name and netid and your teammate's name and netid, at the beginning of the file
* A paragraph describing your contribution, and another paragraph describing your teammate's contribution
    * Please be thorough; we are looking for two substantial paragraphs, not a sentence or two
* A description of whatever help (if any) you received from other people while doing the assignment
* A description of the sources of information that you used while doing the assignment, that are not direct help from other people
* An indication of how much time you spent doing the assignment, rounded to the nearest hour
* Your assessment of the assignment:
    * Did it help you to learn?
    * What did it help you to learn?
    * Do you have any suggestions for improvement? *Etc.*
* (Optionally) Any information that will help us to grade your work in the most favorable light
    * In particular, describe all known bugs and explain why any pylint style warnings you received are unavoidable or why you know better than pylint (a convincing argument may negate some pylint style penalties you accrue)

Your README file must be a plain text file: don't create it using Microsoft Word or any other word processor, although you are encouraged to format it using [markdown](https://www.markdownguide.org/) tags.

Package your assignment files by [creating a release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) on GitHub in your assignment repository.
There must be at least the following files with the following (exact) names in that repository when you submit it:

* `README.md`
* `runserver.py`

Ensure that any additional files needed by your program (such as other Python modules or HTML files) are in the repository snapshot captured by the release.
The one exception to this, as has been the case all semester, is that `lux.sqlite` should *not* be included in your repository.

> **Note**: If you have installed external packages, you must also include a file named `requirements.txt` containing the dependencies of your project.
> It can be created from your virtual environment by running the following command:
> ```
> $ pip freeze -r requirements.txt
> ```
>
> Failure to include a `requirements.txt` file if you use third-party packages will result in an automatic 5% penalty and a request that you submit an appropriate `requirements.txt` file to the graders.

Submit your solution to Canvas (in the assignment named "Web Version A") as [a link to that release](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases).

As noted above in the [Rules](#rules) section, it must be the case that either you submit all of your team’s files or your teammate submits all of your team’s files.
(It must not be the case that you submit some of your team’s files and your teammate submits some of your team’s files.)
You and your team may submit multiple times; we will grade the latest files that you submit before the deadline unless a particular version is requested as the canonical version.

**Please follow the directions on what to submit and how.**
It will be a big help to us if you get the filenames right and submit exactly what’s asked for.
Thanks.

### Late Submissions

The deadline for this assignment is **11:59 PM NHT (New Haven Time) on Friday Nov 3, 2022**.
There is a strict 15 minute grace period beyond the deadline, to be used in case of technical or administrative difficulties, and not for putting final touches on your solution.
(If you can do it in as little as 15 minutes, it probably is insignificant enough not to change your grade.)

Late submissions will receive a 5% deduction for every 12-hour period (or part thereof) after the deadline.
After 72 hours, the Canvas assignment will close and submissions after that time will not receive any credit.

Except for submissions after the 72-hour deadline (*which are not accepted*), the timestamp on the commit associated with the linked release will determine what late penalties, if any, are applied.

---

### Grading

Your grade will be based upon:

* Correctness, that is, how closely your programs conform to the specifications in this document.
* Style, that is, the quality of your program style. This includes not only style as qualitatively assessed by the graders (including modularity, cleanliness, and algorithmic efficiency) but also style as reported by the pylint tool, using the default settings, and when executed via the command `python -m pylint **/*.py`.
    * Ten percent of your grade will be based upon the quality of your program style as reported by pylint. Your grader will start with the 10-point score reported by pylint. Your pylint style grade is your pylint score rounded up to the next integer (minimum 0). For example, if your pylint score is 9.1, then your pylint style grade will be 10; if your pylint score is 7.7, then your pylint style grade will be 8.

If your code fails the tests on some particular functionality, your grader will inspect your code manually to try to assign partial credit for that functionality.
Partial credit will be given only if there is an *obvious* "quick fix" (*e.g.*, you have accidentally changed the name of the database file and your solution points to a file with a name that does not match the grader's copy of the database); if no such quick fix exists then no partial credit for that feature will be given.

---

Adapted from Assignment 3 for COS 333 &copy;2021 by Robert M. Dondero, Jr., Princeton university

Modified &copy;2023 by Alan Weide, Yale University
