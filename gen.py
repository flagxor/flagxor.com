#!/usr/bin/python

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SHOWN_ARTICLES = 4

ARTICLES = [
  {
    'title': 'Source Code',
    'date': 'February 19, 2015',
    'topics': ['Forth', 'Programming Languages'],
    'summary': """\
<p>
Source code, while a common property of programming languages,
is by no mean universal. Languages like Smalltalk, traditional
interactive BASICs, and some Forths often have "source of truth"
representations other than text files. Additional REPLs of all sorts
often retain program state that exists only for the duration
of an interactive session. What are the trade-offs and why does text
continue to be the dominant format?
</p>
""",
    'rest': """\
<p>
A key feature of early micro-computers was an integrated BASIC that contained
not only an interpreter, but an integrated editor. While a few micro-computer
BASICs stored raw program text, the majority stored your program as some
combination of text and pre-parsed tokens.
This was partially due to fact most of the early BASICs were descended from
or inspired by either
<a href="http://en.wikipedia.org/wiki/Tiny_BASIC">Tiny BASIC</a>
or
<a href="http://en.wikipedia.org/wiki/Microsoft_BASIC">Microsoft BASIC</a>.
But it was also likely the result of a desire to save memory on resource
constrained devices.
</p>
<p>
Remarkably, this design choice had several added benefits.
Programs were often "automatically" reformatted to a consistent style,
as post-parsed results often eliminated things like extra whitespace,
or reintroduced it but with a consistent style.
Early refactoring tools, like line renumbering, were easier to implement
when programs were stored as an in memory linked list.
</p>
<p>
Smalltalk and Self apply an even more pure "sourceless" approach
in which classes or prototypes are primarily represented as in-memory
data structures. This has the advantage, and the drawback,
of program code being stored as a memory snapshot.
</p>
<p>
Some Forths have experimented in this direction. A few experimental
Forths are purely sourceless. But more often Forths have explored
using pre-parsed representations.
<a href="http://en.wikipedia.org/wiki/Open_Firmware">Open Firmware</a>
used a representation (FCode) in which each word was pre-parsed
into a number.
<a href="http://en.wikipedia.org/wiki/ColorForth">Color Forth</a>
stores each Forth word as a 32-bit Huffman encode, color tagged
value.
In both cases, however, a interpretation phase actually
compiles / interprets these formats and populates the runtime
Forth dictionary.
Nonetheless, most quality direct / indirect threaded Forths
implement a "SEE" word which
can effectively decompile / disassemble word definitions at runtime,
usually with a high degree of reliability.
</p>
<p>
In my own Forth explorations, I've often struggled with the tension
between the value of source code and the value of having Forth's
runtime state be the source of truth.
Falling back to source code, be it plain text, or a pre-parsed
format has the advantage of preserving the bootstrapping process
in a changeable form. Image based systems, as is typical of Smalltalk
have the odd property that the lineage of a system is often embedded
in the whole system snapshot. Bootstrapping a new variant
involves starting with an existing Smalltalk
image and evolving it to a new desired state.
Just as I try to avoid carrying with me a complex .vimrc file,
I chafe at the idea of my programming environment being
a weathered thing carrying its baggage along.
This seems to run very much counter to the idea of starting something new.
</p>
<p>
Pre-parsed representations have the appeal of making some kinds
of automatic refactoring easier to perform in software robustly.
But the danger is that one needs at least basic
tooling to create such a representation when bootstrapping
or migrating.
When
<a href="http://en.wikipedia.org/wiki/IBM_BASIC">BASICA</a>
transitioned to
<a href="http://en.wikipedia.org/wiki/GW-BASIC">GWBasic</a>
their shared token format meant things went smoothly.
However, the transition to
<a href="http://en.wikipedia.org/wiki/QBasic">QBasic</a>,
which abandoned tokenized source files in favor of plain text,
was a jarring transition. A copy of the old interpreter
was required, so that you could export to plain text.
The new interpreter simply did not support the old format.
</p>
<p>
A related issue with Forth is the question of source code files vs
source code blocks. More bare to the metal Forths, particularly ones
that run without an operating system are known to use 1KB data blocks
displayed in a 64x16 area as the atomic unit of source code.
This has many nice properties: a file system is not required,
line and screen editors are dramatically easier to implement,
and the artistic constraint of a fixed size page makes for very
readable, consistent, and succinct program text.
Tooling for editing or conversion is usually easy to construct.
The drawback is that the format is non-standard,
and potentially wasteful. Also, while all block programs can be
converted losslessly to files, the reverse is not true (at least not trivially).
</p>
<p>
A common practice with block editors is the use of so-called shadow
blocks. Blocks are handled as a pair, one for source code, the other for
comments. The two are either displayed side by side, or a toggle button
shifts from one to the other.
This has the advantage of allowing free form comments in the shadow block.
Also printouts of source code have the nice property that the source
and shadow blocks, at a reasonable font size, can sit side by side in a listing.
The approach is likely also popular because a 64x16 region is
a fairly tight space when comments are inline.
I personally find shadow blocks unpleasant, but that seems to be
a minority view.
</p>
<p>
I am frequently tempted to devise my own text editor.
For my various experimental Forths, I've implemented reasonably
decent block editors, usually in 4-10 blocks of code.
A general text editor is obviously more daunting.
What usually stops me from commencing in earnest is that contrast.
A block editor, being surprisingly easy to implement to a level of
quality that would make it pleasant enough to use daily,
seems like the right idea. Unfortunately, relatively little of my
day to day text processing is with blocks.
</p>
<p>
I'm occasionally tempted to impose a block editing style on file editing.
I imagine some interchange between the two might be possible,
cleverly marking line continuations in some machine decodable style.
Most source code I deal with is 80 column. An 80x25 sized block might
help make this work.
</p>
<p>
Forth is dangerously close to being a language that could be
sourceless. It's dictionary, particularly in simpler threaded Forths,
is very close to isomorphic with the source code.
In my mind there are two main issues with going there.
First, often Forth takes advantage of redefining words so that they
mean different things in different contexts. I certainly have done this
in my programs. But usually I feel like something is wrong when I do it.
The other problem is the dictionary format itself.
While most Forth dictionaries are fairly similar,
I've never really been happy with them.
As Chuck Moore pointed out in a quote in
<a href="http://thinking-forth.sourceforge.net/">Thinking Forth</a>,
the Forth dictionary is often the most complicated data structure
in a Forth system. That complexity, at least in a Forth context,
feels wrong.
</p>
<p>
The potential advantages of a sourceless Forth are tempting, however.
"Good" Forth programs consist of lots of 1-2 line definitions.
It's tempting to think that seeing the context of a given definition
(in the sense of showing the definitions of the words used to define
it and the words that use it), would be nice.
However, the experience with blocks in particular, suggests this might
not pan out. Part of the asthetic appeal of blocks is that they can
be formatted in two dimensions, without consideration of carriage returns.
It's unlikely that automatic methods will have quite the same flare,
regardless of how cleverly contextual they are.
Auto-complete is nice when searching, but likely not when reading code.
<a href="http://en.wikipedia.org/wiki/Literate_programming">
Literate Programming</a> would also seem to suggest that limiting the location
of definitions based on use doesn't fit the narrative style of the human
mind. It's hard to say with certainty without trying it.
</p>
<p>
All of this seems to suggest that source code is here to stay.
Relatively little has crept in beyond ASCII.
Remarkably, we did get beyond programming languages
printable with a
<a href="http://en.wikipedia.org/wiki/IBM_Selectric_typewriter">Selectric</a>
typeball font.
Though the continued precence of
<a href="http://en.wikipedia.org/wiki/Digraphs_and_trigraphs">Trigraphs</a>
in C++ would seem to contradict this to some degree.
I wish for more in my source format at times (particularly color
or perhaps limited font control), but just as often I wish for less
in the form of blocks.
I think I should console myself with the fact we've somehow managed
to stick with a minimalistic format like text for source code.
So few things in software are minimal these days after all.
</p>
""",
  },
  {
    'title': 'Why do Programming Languages Succeed?',
    'date': 'December 20, 2014',
    'topics': ['Forth', 'Programming Languages'],
    'summary': """\
<p>
There have been thousands of programming languages of various scopes created
since the advent of computers. Of these, two kinds are worthy of special
attention: those that are very popular and those that are very original.
Perhaps not remarkably, both groups are quite small. A few languages probably
belong in both categories.
</p>
""",
    'rest': """\
<p>
Popularity is relatively unambiguous. However, the growth of the software
industry means that the number of developers that made Fortran popular is tiny
in comparison to JavaScript.
</p>
<p>
Measuring originality, on the other hand, is complicated by the fact that novel
ideas are often only recognized as significant in hindsight. For example, while
Simula predates Smalltalk, which in turn predates Self, it's debatable which of
these languages best embodies the unique constellation of ideas surrounding
object-oriented programming. Unsurprisingly, as the low hanging fruit has
mostly been picked, many of the most novel languages are also relatively old.
</p>
<p>
Obviously granting some subjectivity on originality and guesswork due to lack
of historical statistics on popularity, below are my lists. Those in both
categories are starred. The original languages are tagged with a description of
what makes them special. Some of the original languages share the title when
there isn't a clear exemplar. Also, I don't mean to suggest that un-starred
unique languages haven't achieved some degree of popularity. Often they have
loyal followings, are taught in advanced institutions, or have been used for
something big, but generally they aren't used widely for day to day
development. The cut off for being popular enough is similarly squish. If I've
left off your favorite, I apologise.
</p>
<p>
<h4>Very Popular</h4>
<ul>
  <li>Ada</li>
  <li>ActionScript</li>
  <li>BASIC / Visual Basic / VBscript / ASP</li>
  <li>C *</li>
  <li>C++</li>
  <li>C#</li>
  <li>COBOL</li>
  <li>Fortran *</li>
  <li>Hypercard *</li>
  <li>Java</li>
  <li>JavaScript</li>
  <li>Logo</li>
  <li>Lua</li>
  <li>Matlab / R</li>
  <li>Objective C</li>
  <li>Perl</li>
  <li>Python</li>
  <li>Ruby</li>
  <li>Pascal</li>
  <li>PHP</li>
  <li>Shell / Bash</li>
  <li>SQL *</li>
  <li>Tcl/Tk</li>
</ul>

<h4>Very Original</h4>
<ul>
  <li>Algol - Structured Programming</li>
  <li>APL - Everything is a Tensor</li>
  <li>Fortran * - High Level Languages</li>
  <li>Forth - RPN, Compile Time Execution, Everything a Word</li>
  <li>Haskell - Pattern Matching, Monads</li>
  <li>HyperCard * - Code bound to widgets</li>
  <li>Inform7 - Strong Literate Programming</li>
  <li>Lisp - Data as Code, Functional Programming</li>
  <li>PL/I / C * - Pointers and Pointer Arithmetic</li>
  <li>Prolog - Logic Programming</li>
  <li>Simula / Smalltalk / Self - Object Oriented Programming</li>
  <li>SQL* - Relational Databases</li>
</ul>

<hr/>

<h3>Popularity</h3>

<p>
Popular languages, share some common themes surrounding why they became
popular. Broadly these themes are: Easy to Embedded, Easy to Implement, Scoped
for Teaching, Powerful or Unique Libraries, Powerful Built-In Types /
Operators, Endorsement of a Powerful Entity / Gateway to a Platform,
Intertwined with the Success of UNIX.
</p>

<h4>Easy to Embedded</h4>
<ul>
  <li>BASIC</li>
  <li>Lua</li>
  <li>Python</li>
  <li>Tcl</li>
</ul>

<p>
Ease of embedding seems to help spread languages by creating a bunch of niche
contexts in which learning the embedded language becomes the only way to use a
tool. Lua and Tcl as well as Python in its early days found their way into Game
Engines, Graphics tools, Web Servers, and Window Managers as a configuration /
extension languages. BASIC or a subset of it, is a regular feature in Word
Processor and Spreadsheet expression and scripting languages.
</p>

<h4>Easy to Implement</h4>
<ul>
  <li>BASIC</li>
  <li>Pascal</li>
</ul>

<p>
Ease of implementation played a significant role in language popularity,
particularly during the early microcomputer era. A small memory footprint with
implementations often small enough to be printable in a magazine allowed BASIC
to spread to most early systems. Similarly Pascal's small grammar allowed
compact implementations for very early systems, as well as highly performant
implementations like Turbo Pascal.
</p>

<h4>Scoped for Teaching</h4>
<ul>
  <li>BASIC</li>
  <li>Logo</li>
  <li>Pascal</li>
  <li>Python</li>
  <li>Java</li>
</ul>

<p>
Being scoped for teaching helps spread languages by shaping the preferences of
newly minted programmers. Teaching material for BASIC and Logo were pervasive
during the early 1980s push to teach kids to code. Pascal took over once
unstructured programming had fallen out of fashion. Java and later Python made
fast inroads in education by providing syntactically small but contemporary
object-oriented languages that include key CS teaching features like built-in
concurrency. Each has a relatively definitive dialect or sub-dialect teachable
in the span of a single course. Arguably, standardization plays a central role,
as very popular languages like C++ often find use in education only when
coupled with an extensive cross-course library. Also, it's notable that
teachability often popularizes only a subset of a language. Logo's capabilities
beyond turtle graphics were rarely taught, and only small portion of Python and
Java libraries are commonly explored in an education setting.
</p>

<h4>Powerful or Unique Libraries</h4>
<ul>
  <li>Java - Large standard library</li>
  <li>Python - Large standard library</li>
  <li>Ruby - Rails</li>
  <li>Tcl/Tk - Tk!</li>
</ul>

<p>
A useful library can make a language. The brief popularity of Tcl was almost
entirely fueled by the Tk graphics library. Rails made Ruby. Python and Java
benefit from huge standard libraries as well as a cornucopia of freely
available additional libraries. Libraries that are cross-platform seem to play
an oversized role, as people will often tolerate a new way of programming if it
gives them reach. Being the only game in town seems to matter. Tcl's popularity
rapidly deflated once Tk and equivalents became available for other languages.
Many relatively unpopular languages now have a range of libraries that once
would have been considered large, but which come up short in light of the
number available for currently popular languages.
</p>

<h4>Powerful Built-in Types / Operators</h4>
<ul>
  <li>BASIC - Strings</li>
  <li>COBOL - Structures / Records</li>
  <li>Fortran - Complex Numbers + Arrays</li>
  <li>Hypercard + Visual BASIC - GUI built-in</li>
  <li>Java - Concurrency</li>
  <li>Logo - Turtle Graphics</li>
  <li>Matlab / R - Matrix Operations</li>
  <li>Objective C + C++ - Objects</li>
  <li>Perl - Regular Expressions</li>
  <li>PHP - CGI out of the box</li>
  <li>Python + Ruby + Javascript - JSON (strings, lists, maps)</li>
  <li>Shell / Bash - Pipes + Redirection</li>
  <li>SQL - Relational Algebra</li>
</ul>

<p>
Being able to express a particular domain succinctly seems to matter. Regular
expressions were the killer feature for Perl, so much so that Perl style regexs
pervade other languages and tools. Decent string operations helped early BASIC.
Standardize graphics primitives made Logo. Fortran was made by arrays and
complex numbers. Standard memory and disk structures were why people wanted to
use COBOL. Shell scripts gave uses access to the power of pipes and
redirection. HTML inline with code in PHP helped web designers step
incrementally from static pages to dynamic ones. Hypercard let non-programmers
have a hand at UI design. The success of relational databases and SQL was
intertwined. Concurrency out of box helped Java.
</p>
<p>
In some cases, popular languages spread the features of the unique languages
outside their narrow communities:
<ul>
  <li>Hypercard &rarrow; Visual BASIC --- GUI built-in</li>
  <li>Lisp &rarrow; Logo (unsuccessfully), Python + Ruby + Javascript
      --- Weak Functional Programming</li>
  <li>APL &rarrow; Matlab/R -- Matrices / Tensors</li>
  <li>Simula / Smalltalk / Self &rarrow; Objective C + C++ --- Objects</li>
</ul>
</p>

<p>
Building things into the core syntax of a language seem to matter. This is
likely both because it allows for syntactic sugar (reducing noise), and because
it means there is a definitive way to express something. Reducing an idea to
the point it has a good notation is usually an indication the idea is ready for
dissemination. Perl's regexes, Matlab's matrices, Python's list comprehensions,
BASIC's strings, Fortran's complex numbers, COBOL's structures all have in
common that they represent the point when an idea found a notation good enough
that you'd write it on a blackboard. 
</p>
<p>
Languages that don't build in these constructs often imitate them with an
almost sad deference to their original source. Much of the evolution of C++ can
be seen as a quest to allow Fortran style complex numbers, BASIC style strings,
COBOL style serialization, and Matlab style matrices to be implemented as
libraries. A host of languages embed a clone of Perl's regex syntax, but
stubbornly embed it in a string, often at higher runtime cost, and usually with
vexing escaping quirks.
</p>

<h4>Endorsement of Powerful Entity / Only Way to Program a Platform</h4>
<ul>
  <li>ActionScript - Flash</li>
  <li>Ada - Department of Defense</li>
  <li>BASIC / Visual Basic / VBscript / ASP - Microsoft</li>
  <li>C++ - Microsoft</li>
  <li>C# - Microsoft</li>
  <li>Fortran - IBM</li>
  <li>Objective C - Apple</li>
  <li>JavaScript - The Web / Google / Mozilla</li>
</ul>

<p>
Some languages benefit from a powerful sponsor. These languages are, or were at
some point, the only way to program for a popular platform or audience, or the
only "recommended" way. Though their users are captive, the languages aren't
always terrible. Often languages in this category improve over time, if they
started out bad, to prevent alternate contenders from stealing the reins. The
effect of the sponsor is often amplified when a sizable user community develops
around a language.
</p>

<h4>Intertwined with the Success of UNIX</h4>
<ul>
  <li>C</li>
  <li>Shell / Bash</li>
</ul>

<p>
The success of UNIX is fairly unique in computing. Prior to UNIX, operating
systems failed to succeed in definitively standardizing I/O, process control,
and interprocess communication. Often language specific standards for I/O
trumped OS ones. After UNIX, other operating systems frequently have mimicked
its facilities, sometimes fixing their rough edges, but more often watering
them down or making them more complicated. C is a fairly ideal language to
implement the core parts of a UNIX system. Shell scripts combined with a
collection of micro-applications form a domain specific process control
language that's just as much a part of UNIX as its standard syscalls. Thus C
and shell scripts are intertwined with the success of UNIX and the UNIX model
of an OS, making their success mutual.
</p>

<hr/>

<h3>Originality</h3>

<p>
What make the "original" languages original, is that they each introduced a new
programming paradigm.
</p>
<p>
Conventional wisdom has a played an oversized role in which of these language's
ideas have spread. A sizeable portion of developers hold the belief that we've
progressed from low level, to high level (Fortran), to structured (Algol), to
object oriented (Simula / Smalltalk / Self) programming. Many have also seen
the wisdom of mixing in functional programming (Lisp) constructs when possible.
Interestingly, with the exception of Fortran, none of the languages responsible
for introducing the most widely accepted paradigms actually benefiting by being
first. Fortran's novelty in this regard is likely the result of its strong
backing from IBM, coupled with it arguably evolving so radically in its early
days, that it became its own successor.
</p>
<p>
All of the starred languages (both popular and original) intriguingly appear in
the "Powerful Built-in Types / Operators" category above. This suggests that
devising the "right" notation for something can be so compelling that it makes
your language. These language, Fortran, C, Hypercard, and SQL also could be
said to have benefitted from being part of a larger movement Fortran
(scientific computing), C (UNIX), Hypercard (GUIs), SQL (standardization of
relational databases).
</p>
<p>
By contrast the languages that introduced a successful paradigm, but failed to
capitalize on it, seem to suffer from a variety of weaknesses. APL's succinct
notation, while appealing to strong mathematicians, was hampered by its steep
learning curve in the hands of weak ones. The burden of a quirky character set,
probably also kept it out of enough hands to hold on to its killer feature.
Matlab succeed in the same domain with a more friendly learning curve for
novices. Algol while the Ur-structured programming language, was notoriously
difficult to implement, leaving open the door for languages like Pascal and C.
Lisp's functional programming was conflated with the orthogonal idea of code as
data, thus hampering its dissemination with a tedious syntax. Simula,
Smalltalk, and Self suffered from being invented at moments in time when the
runtime cost of dynamic dispatch was prohibitive on mainframes and
microcomputers respectively.
</p>
<p>
Some paradigms exemplified by the special languages are arguably unrealized or
aspirational. Lisp's notion of code as data seems profound, but is hard to
apply in practice. Also, Lisp programs are often no more strictly functional
than a typical Python or Perl program. Prolog's logic programming is really an
attempt to apply a theorem solver to general purpose programming, but actual
Prolog programs are written with implicit assumptions about evaluation, Lisp in
disguise. Haskell's pattern matching and monads end up being used mostly as a
vehicle to embed imperative programs. Inform7's natural language use is
compelling in a subset of the adventure game domain, but falls short in COBOL
like ways outside it. Forth's compile time execution, which is also being
experimented with in C++ via template meta-programming, has generally failed to
be made convenient enough for everyday use by non-experts. Forth's potential
for extreme refactoring (particularly into one line definitions) is in practice
used by a limited subset of very skilled users. The majority of Forth programs
are not that different from C programs written with heavy use of statics /
globals and limited use of types, locals, and parameter passing. In each case,
the paradigm may yet lead somewhere, but arguably we haven't yet found the
right notation or figured out how to actually program in the paradigm.
</p>
<p>
This implies an interesting test if you think you've got a cool new programming
language paradigm:
</p>

<div style="background: #efe; margin: 20px; padding: 20px;">
<h3>Flagxor's Rockstar Test</h3>
<p>
<b><i>
A programming language paradigm is real only if code written by an average user
of the language looks pretty close to code written by experts.
</i></b>
</p>
</div>

<hr/>

<h3>What didn't matter</h3>

<p>
It's also interesting to examine what didn't matter.
</p>
<p>
The ability to embed domain specific languages in Lisp and Forth seems to have
been overwhelmed by the fragmentation resulting from everyone doing it
differently. Forth and Lisp have multiple libraries for implementing things
like regexs, numeric data, or object oriented behavior. While Forth and Lisp
can often borrow use notational styles from other languages with high fidelity,
subtle incompatibilities and slow or inconclusive standardization undermine
this flexibility in practice.
</p>

<hr/>

<h3>How to succeed in programming languages...</h3>

<p>
So what would it take today to popularize a language? You'll get a temporary
boost if you make it easy to embed in other tools or come up with some unique
or elegant libraries for it. Making it easy to implement might give you the
benefit of competition, but as long as your implementation is portable and of
good quality, it might not matter in this day in age. You could pitch it as a
learning language or get a big corporate sponsor, but be careful not to make it
too novel or you'll weed yourself out. Alternatively if you want your language
to actually be special, your best bet looks like to come up with really good
notation to express some problem domain, and then bake it in. In all cases, be
sure to have a standard library up to todays standards, and be sure to support
structured, object oriented, and a dash of functional programming.
</p>

<h4>Plan A: (Ruby / Groovy / Dart / Java / Swift / Python / C++...)</h4>
<p>
Make your language a rationalization of existing practice, knock off all the
other cool kids. Beg borrow and steal libraries and lock in corporate or
scholastic backers.
</p>

<h4>Plan B: (Road less travelled...)</h4>
<p>
Come up with the perfect syntax for some ill served domain. This is pretty much
as hard as devising an "original" language. Next, bake the syntax into a
language that keeps all the imperative programming features the world loves,
with a syntax as close as possible to the mainstream. Then, do most of the
other stuff from A.
</p>
<p>
Plan A has the disheartening drawback that you're not really inventing anything
so much as making a mash-up. Plan B suffers from all the same hardships, with
the added problem of coming up with a notation for something new. You also, of
course, have the option of inventing a weird new trick language and letting
someone else bring your secret sauce to the masses.
</p>
<p>
I confess I lack the even temperament and soul crushing conformity required for
Plan A. While Plan B sound daunting, I actually find it somewhat hopeful. It
usefully clarifies what you need to do get there. Aside from possibly getting
the backing of a Fortune 500 company or nation state and all the work of
actually implementing your language and the mountain of libraries you need to
get the ball rolling, you're really just in the business of inventing an
algebra for something that's not currently covered well. How hard could that
be?
</p>
""",
  },
  {
    'title': 'Multiple Prototypes',
    'date': 'October 14, 2014',
    'topics': ['Programming Languages'],
    'summary': """\
<p>
While early prototype based languages like Self
and NewtonScript allowed multiple-prototypes, Javascript only allows
a single prototype per object. I'll explore the trade-offs
of each approach, rant vaguely.
</p>
""",
    'rest': """\
<p>
Prototype based languages use a variation on object oriented programming.
Rather than use an inheritance hierarchy of classes,
prototype based languages use the notion that an object can express
just what makes it unique and then reference one or more "prototypes".
These prototypes are just other objects.
Give or take issues around initialization and mutation,
a conventional class hierarchy can be approximated by expressing classes
as prototypes themselves in a hierarchy, referenced by each instance.
However, part of the appeal of the approach is that it is ideally more
flexible than a traditional static class hierarchy, allowing for
possibilities like "dynamic inheritance".
</p>
<p>
The original prototype based language (and probably its most pure form
of expression) is the
<a href="http://en.wikipedia.org/wiki/Self_(programming_language)">
Self programming language</a>.
Everything in Self, down to activation frames for parameter passing
is a collection of key value pairs in which special keys (marked with
an asterisk *) are prototypes, which can be assigned a precedence.
All parent trees are traversed when deciding how to resolve a key,
if two equal precedence resolutions are possible, an error is thrown.
This allows for multiple inheritance, with semi-sane conflict resolution.
</p>
<p>
<a href="http://en.wikipedia.org/wiki/NewtonScript">NewtonScript</a>,
the programming language for the Apple Newton,
was inspired by a desire to fit Self into the constraints of a 128KB
device. Self like chaining was viewed as a way to compress the size
of objects as well as a flexible implementation choice.
One simplification made, was that rather than allowing an unlimited
number of prototypes, two are allowed: _proto, _parent.
_proto has a higher precedence than _parent. This allowed for _proto
to fill a traditional inheritance role, and _parent to allow GUI widgets
to propagate un-handled events up to their parent.
Unlike Self, this would not allow direct simulation of multiple
inheritance. Offhand it seems like the weaker notion of a set of
standalone mix-ins might be possible, by creating a chain of mix-ins
using _proto and _parent to build list chains, much like (car, cdr) to cons'es in Lisp. Strictly this could probably also approximate multiple
inheritance generally, with the requirement that parent classes would
have to have a strict precedence order.
</p>
<p>
Javascript in turn allows only a single prototype for each object.
An object o has o.__proto__ which its runtime prototype.
This is in turn a reference to whatever was in some Function.prototype
when new was called. Raw data objects {data: 1} are prototype-less.
This has the advantage of simplicity, but requires copying of methods
to simulate multiple inheritance.
</p>
<p>
One appeal of the Javascript approach is that while it requires a decent
amount of careful upfront copying, it can do most multiple inheritance like
behavior that a static class hierarchy would allow. Dynamic inheritance
is probably playing with fire.
The unappealing downside is that the object prototype hierarchy doesn't
reflect programmer intention, but rather the result of copying methods
as needed.
This is less of an issue in Javascript than it would be in Self, where
objects are dynamically edited and the world pickled to a system image.
</p>
<p>
The Self rules for resolving conflicts seem baroque
and arbitrary. NewtonScript allows something as flexible, if you are
willing to replace n-fanout with multiple 2-fanout branches.
Javascript requires copying, but is the simplest.
</p>
<p>
I wonder if anyone has done a prototyping language which handles
the prototype by calling an un-handled message slot with messages
to delegate. Yea old Internet says Squeak Smalltalk can do this
via ObjectTracer, but that sounds like a slow debugging type interface
not something you'd want every message to pass through.
I would imagine Self's "implicit" delegation was probably motivated
by the many performance optimizations it can do, pointing to the same
conclusion.
</p>
""",
  },
  {
    'title': 'HTML templates, Python vs Javascript, Escaping',
    'date': 'October 3, 2014',
    'topics': ['Programming Languages', 'Blogging'],
    'summary': """\
<p>
My blog's Static HTML has now been replaced with a python generation
script. I shall now pontificate on escaping, Python vs Javascript,
and lament how to handle more articles.
</p>
""",
    'rest': """\
<p>
On adding the 4th article, it of course becomes clear that manually
copying a static HTML template will never do. I knew this before,
but deferred the issue. I migrated by chopping up the articles I have
into multi-line python strings embedded in a JSON-y list of articles.
While I originally considered putting each article in a separate file,
this seemed simpler. Also I hold a long-standing speculation that the
right way to deal with complexity isn't to chop up things into lots
of little files, but to fix your editor (insert clever idea).
Though in practice I hate big files, so we'll see how long this lasts.
</p>
<p>
Having everything in one big structure lets me also generate an index.
While I currently have so few articles that dumping them in reverse
order works, that won't scale.
I start by duplicating what I have, and generating it on top of the
existing static files. With git that lets me check that nothing
has changed too drastically.
</p>
<p>
To plan ahead for lots of articles (you never know), I've added a subjects
fields to each article. This way I can generate a title only subject index.
I think I'll do two, one by just date, the other by subject.
</p>
<p>
For templates I've used Python's % operator.
This works surprisingly well as HTML + Javascript generally don't make
much use of %. Mod-ing is apparently unpopular :-(.
</p>
<p>
Python's multi-line quotes shine for this use case,
as they allow me nice chunks of text for summaries and articles.
Javascript lacks the equivalent, unless I've missed it.
</p>
<p>
Of course all of this is folly. It's just more escaping to allow a text
document to stand in for something that's really a more complex entity.
Escaping is the root of all evil.
</p>
""",
  },
  {
    'title': 'Added new blog and forum!',
    'date': 'October 1, 2014',
    'topics': ['Blogging'],
    'summary': """\
<p>
After a long hiatus, I'm making another attempt at semi-regular blogging.
Also, using <a href="http://disqus.com">Disqus</a> I've added forums
to <a href="http://forthsalon.appspot.com">Forth Haiku</a>
and the new <a href="http://flagxor.com">blog</a>.
</p>
""",
    'rest': """\
<p>
My original intention with forthsalon was primarily to publish a blog.
Forth Haikus were an afterthought.
Ultimately, despite adding a good bit of plumbing to support a crude
sort of article editor, only 2 posts ever materialized.
Now, I'm giving it another go.
</p>
<p>
As the Forth Haikus have taken on a bit of a life of their own,
I'm loath to conflate my rantings with the existing traffic.
For now I'm putting the blog on a separate site,
but will probably tie in to Forth Haiku (with an iframe GASP!)
to see if anyone wants to hop over
the gap. Since I now have a comment section, I might hear if this
annoys people.
</p>
<p>
The new blog is titled: Flagxor's Bytes and Bobs.
In the past, I've generally posted as BradN in various contexts.
Unfortunately, that's a bit less that searchable uniquely,
so I'm giving a crack at "owning" the flagxor handle.
Bytes and Bobs seems an underused, though not strictly unique,
play on the common phrase. The two combined are at least sure to be
unique.
</p>
<p>
In starting blogging again, I decided to try a new process.
The old approach of posting articles completely online
via a crude web form fails to match up with my actual goals.
I don't really want a blog that's completely stream of conciousness.
And, at least for now, prefer the idea of being able to retro-actively
fix things.
To that end, for now I'm editing the blog as static html.
I will probably end up scripting the process,
or possibly giving something like
<a href="http://blog.getpelican.com/">Pelican</a> a try.
</p>
<p>
In other news, I've added a comment / forum section to each Forth Haiku
and to each article in the new blog.
<a href="http://eli.thegreenplace.net/">Eli Bendersky's</a> recent
<a href="http://eli.thegreenplace.net/2014/blogging-setup-with-pelican/">switch</a>
from Wordpress to Pelican brought to my attention the existence
of a new sort of service: an embeddable forum called
<a href="http://disqus.com">Disqus</a>.
This service solves several substantial issues that have long blocked
me from adding a forum to Forth Haiku.
</p>
<p>
What I wanted in a forum was the ability to moderate away spam, manage
a per haiku comment section, and to require some sort of authentication
to post. This substantial body of functionality was always at odds with
my desire to keep the main Haiku site and code implemented in fairly
standalone Javascript backed by an equally standalone and simple
Python AppEngine app.
Disqus solves this by allowing each page to emit a small blurb of
Javascript to inject a per-topic discussion area
and by providing a UI to let me nix spam if I decide its worth the bother.
They support the option to download the raw discussion data
in an XML format, so I can at least entertain the notion that I'm
not stuck with them holding the forum data.
Also, while I'd always had a login option
for the Haiku site, this was mainly a way to allow me to authenticate
for article entry. I don't really want to be in the business of asking
for people's login info. Disqus supports
handling authentication with a range of identity providers,
which seems like more likely to convince someone to post comments.
</p>
<p>
Anyhow, time will tell if I keep up momentum.
Wish me luck...
</p>
""",
  },
  {
    'title': 'less is more',
    'date': 'June 20, 2011',
    'topics': ['Forth Haiku'],
    'summary': """\
<p>
A number of recently added standard Forth words have been dropped
from the core vocabulary:
<pre>! @ IF ELSE THEN VARIABLE ALLOT HERE.</pre>
Surprisingly few haikus had to be updated to accommodate,
suggesting not much has been lost.
</p>
""",
    'rest': """\
<p>
I recently added a number of standard Forth words to the Haiku Forth
core word list. Theoretically these words might have allowed interesting
behavior. In practice, only 4 haikus (two of which were derived works)
required updating. In both cases, the result was smaller.
</p>
<p>
The exclusive user of IF, THEN were the two mandelbrot
haikus.
They each contained the sequence:
<pre>dup 0 &lt; if drop 0 then</pre>
This sequence is easily replaced with:
<pre>dup 0 &gt;= *</pre>
And if fact, I now realize, even more tersely:
<pre>0 max</pre>
</p>
<p>
The only user of VARIABLE, @, ! were the two variations of the red ball.
At a small performance penalty, this:
<pre>variable xx x 0.5 - xx ! ... xx @</pre>
was replaced with:
<pre>: xx x 0.5 - ; ... xx</pre>
Fewer total words, and less 'line noise'.
</p>
<p>
Despite my 'ambitions', the words ELSE, HERE, ALLOT were never used.
They were also dropped.
</p>
<p>
As a result of dropping these words, the effort involved in adding
an optimize pass which eliminates the internal use of the dstack + rstack
arrays in favor of temporary variables was greatly reduced.
This optimization noticeably speeds up Android performance,
and is a hearty step towards being able to add WebGL support,
and thereby animation via a 't' word.
</p>
""",
  },
  {
    'title': 'Generating Spirals',
    'date': 'April 22, 2011',
    'topics': ['Forth Haiku'],
    'summary': """\
<p>It turns out a spiral isn't too bad to implement.</p>
""",
    'rest': """\
<p>
The key trick with a spiral is to combine the distance from the center
with the rotation around the center (obtained with atan2).
Once this is obtained, taking the sine can be used to oscillate
along a path that grows outward in a spiral.
</p>
<p>
<a href="http://forthsalon.appspot.com/haiku-view/ahBzfmZvcnRoc2Fsb24taHJkcgsLEgVIYWlrdRgEDA">Example</a>
<pre>
: square dup * ;
: dist square swap square + sqrt ;
: 2dup over over ;
: spiral 0.5 - swap 0.5 - 2dup dist push atan2 0.01 * pop + 100 * sin ;
x y spiral x y spiral x y spiral
</pre>
</p>
""",
  },
]


def main():
  templates_dir = os.path.join(SCRIPT_DIR, 'templates')
  article_template = open(
      os.path.join(templates_dir, 'article.html')).read()
  index_template = open(
      os.path.join(templates_dir, 'index.html')).read()
  header_template = open(
      os.path.join(templates_dir, 'header.html')).read()
  footer_template = open(
      os.path.join(templates_dir, 'footer.html')).read()
  index_article_template = open(
      os.path.join(templates_dir, 'index_article.html')).read()
  archive_article_template = open(
      os.path.join(templates_dir, 'archive_article.html')).read()
  topics_topic_template = open(
      os.path.join(templates_dir, 'topics_topic.html')).read()
  topics_article_template = open(
      os.path.join(templates_dir, 'topics_article.html')).read()
  index_articles = []
  archive_articles = []
  topic_articles = {}
  for article in ARTICLES:
    alt_title = article['title'].lower()
    alt_title = alt_title.replace(' ', '-')
    alt_title = re.sub('[!,?]', '', alt_title)
    article_path = os.path.join(
        SCRIPT_DIR, 'article', alt_title + '.html')
    topic_links = ['<a href="/topics#%s">%s</a>' %
                   (t, t) for t in article['topics']]
    fields = {
        'title': article['title'],
        'alt_title': alt_title,
        'date': article['date'],
        'summary': article['summary'],
        'rest': article['rest'],
        'topics': ', '.join(topic_links),
        'header': header_template,
        'footer': footer_template,
    }
    with open(article_path, 'w') as fh:
      fh.write(article_template % fields)
    index_articles += [index_article_template % fields + '\n']
    archive_articles += [archive_article_template % fields + '\n']
    for topic in article['topics']:
      if topic not in topic_articles:
        topic_articles[topic] = []
      topic_articles[topic] += [topics_article_template % fields + '\n']
  with open(os.path.join(SCRIPT_DIR, 'static', 'index.html'), 'w') as fh:
    fh.write(index_template % {
        'content': ''.join(index_articles[:SHOWN_ARTICLES]),
        'header': header_template,
        'footer': footer_template,
        'subtitle': '',
    })
  with open(os.path.join(SCRIPT_DIR, 'static', 'archive.html'), 'w') as fh:
    fh.write(index_template % {
        'content': ''.join(archive_articles),
        'header': header_template,
        'footer': footer_template,
        'subtitle': '- Archive',
    })
  topics = sorted(topic_articles.keys(), key=lambda s: s.lower())
  topics = [topics_topic_template % {
                'topic': t,
                'articles': ''.join(topic_articles[t]),
           } for t in topics]
  with open(os.path.join(SCRIPT_DIR, 'static', 'topics.html'), 'w') as fh:
    fh.write(index_template % {
        'content': ''.join(topics),
        'header': header_template,
        'footer': footer_template,
        'subtitle': '- By Topic',
    })


if __name__ == '__main__':
  main()
