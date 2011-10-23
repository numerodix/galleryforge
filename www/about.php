<? include("_head.php"); ?>

<h2>About</h2>


<h3>What makes galleryforge different?</h3>

For my own use, I needed something that would:
<ul>
	<li>do all the processing work on the client side,</li>
	<li>to create a bunch of files I can just <a href="http://samba.anu.edu.au/rsync/">rsync</a> to the web server,</li>
	<li>recurse into sub directories,</li>
	<li>give me, if not full control, then at least a lot of control over the look of the pages generated,</li>
	<li>generate valid XHTML code,</li>
	<li>allow me to add albums as I go along,</li>
	<li>and complete the whole process quickly without needing user input along the way.</li>
</ul>


<h3>What's wrong with the alternatives?</h3>

<p>Well, there are a lot of gallery-related projects out there and I reviewed a lot of them before deciding to start my own. Each of them has their own problems and I failed to find one that does exactly what I need it to do, so galleryforge is a project in the typical hacker sense of "scratching an itch". So what is wrong with the others? Broadly speaking, I divide them into the following categories..
</p>

<h4>Web-based galleries</h4>

<p>These are scripts which run on the web server. they let you upload images, they will resize them for you, let you add descriptions, offer several themes for the gallery layout to choose from, allow you to share your gallery with other contributors, allow users to post comments about the images, store all the metadata in a database and so on. Example: <a href="http://gallery.sourceforge.net/">Gallery</a>.
</p>

<p>If you run a gallery with multiple contributors, this is the concept for you. Otherwise, it has some obvious drawbacks. First of all, processing images on the web server is a cpu-intensive process. Depending on the implementation, the script may time out before the processing completes, it may overload the server etc. Secondly, uploading images through a web page is painfully slow and inconvenient. Next, customizing templates usually takes some doing and is not dead simple, given that the pages are sometimes constructed in an elaborate way. Finally, you depend completely on the web server and its integrity. If the database crashes, you may lose your data, so you have to make frequent backups. If you move to a new web host, restoring your site may be non-trivial.
</p>

<p>But most of all, doing it this way is a lot more involved, it takes a lot more time than running galleryforge with pre-set settings.
</p>

<h4>Gallery generator scripts</h4>

<p>These are more old fashion projects, similar to galleryforge. You give it a directory containing images and it will create an album for you. Various projects offer various degress of customization for the output HTML. Example: <a href="http://mkgallery.sourceforge.net/">MkGallery</a>.
</p>

<p>The basic drawback with this model is that I have yet to see a script which will recurse into sub directories, all these scripts are made for a single album only. Of course one could run them multiple times, but if I'm scripting the script anyway, rolling my own doesn't take a lot more doing, while giving me much more control. Another thing is that a lot of these scripts generate pretty shoddy HTML, to fix that one would have to hack the script, unless it provides templates.
</p>


<h3>Why doesn't galleryforge have &lt;feature&gt; and the kitchen sink?</h3>

<p>It's not terribly hard to imagine that galleryforge could be extended with an ftp client to publish albums, an image viewer to make management of photos easier, some basic imaging tools like scaling and cropping, an editor to handle the templates and so on. In fact, there are tools out there which do things like that.
</p>

<p>Instead, galleryforge attempts to stay true to the old Unix dictum "do only one thing, and do it well". Why add an ftp upload feature without support for sftp? What if the user <i>does</i> want to use sftp? Instead of adding all sorts of things that may (yet may not) be useful, galleryforge strives to be good at creating galleries, and nothing more. This leaves the user to decide how to edit templates, how to transfer files and so on.
</p>

<p>In its core business, galleryforge aims to offer choice (supports various file formats, offers plenty of options, both console and gui interface) and flexibility (editable templates, multiple albums). Features which would improve galleryforge's core value will be considered, peripheral features won't be.
</p>


<h3>How is galleryforge implemented?</h3>

<p>The basic functionality (scanning for images, resizing, renaming them, making thumbnails etc), was coded in a day, in Python, using the Python Imaging Library. And that was all galleryforge really needed, but I decided it would be easier to understand and use if it had a gui, so I drew up a gui in wxGlade and generated Python code. At the time, I had heard good things about test-first programming and although I didn't write the tests beforehand, I did write tests for the basic functionality, you can execute <i>galleryforge/test/testall.py</i> to run the whole test suite.
</p>

<p>The code is supposed to be fairly platform independent, I've tested it on Linux and WindowsXP and written an installer script as well. For Gentoo Linux, there is an ebuild in <i>install/</i>.
</p>


<h3>Is there any documentation?</h3>

<p>No more than necessary.. ;-) In <i>doc/</i>, there is an <i>INSTALL</i> and a <i>README</i> file, both of which describe all you have to know to install and use galleryforge.
</p>


<h3>Who is behind galleryforge?</h3>

<p>Martin Matusiak &lt;numerodix at users.berlios.de&gt;
</p>

<? include("_foot.php"); ?>