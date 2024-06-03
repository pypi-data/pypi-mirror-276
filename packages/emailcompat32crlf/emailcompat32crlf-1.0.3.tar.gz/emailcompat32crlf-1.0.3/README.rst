Default to CRLF policy for compat32 emails
==========================================

This is a minimal package. It patches the standard lib, so that it defaults to using
``\r\n`` as line endings, instead of the standard lib default ``\n``.

Doing so makes emitted emails standards compliant.

Moreover, doing so avoids getting corrupted emails delivered when relaying emails via
outlook.com or office365.com.

The problem this package fixes, shows up as quoted-printable soft line endings
``=\n`` getting transformed into encoded equals signs ``=3D`` plus the removal
of the first character following the newline. If you have URLs straddling a newline,
those will not be valid anymore. But also normal text gets broken.

Email policies
--------------

We patch the ``Compat32`` policy class and its ``compat32`` instance.
There are other policies, like the ``EmailPolicy`` class (using ``\n`` as line separator) and its `SMTP` instance (using ``\r\n`` as line separator).  We do not touch those.

Quoting from the `email.policy documentation <https://docs.python.org/3/library/email.policy.html>`_:

* There is a default policy used by all classes in the email package. For all of the parser classes and the related convenience functions, and for the Message class, this is the ``Compat32`` policy, via its corresponding pre-defined instance ``compat32``. This policy provides for complete backward compatibility (in some cases, including bug compatibility) with the pre-Python3.3 version of the email package.
* The default value for the policy keyword to ``EmailMessage`` is the ``EmailPolicy`` policy, via its pre-defined instance ``default``.


Why patch the standard lib, instead of fixing your own code?
------------------------------------------------------------

Because to fix your own code, you'd have to ensure to override the default
policy in every single instantiation of every ``Message`` or ``MIMEText`` or any
of the other constructors which default to the ``compat32`` policy
without carriage returns.

Instead, you now can simply add ``emailcompat32crlf`` to your project dependencies and import it. Done.

If you are using Plone: we register an autoinclude entry point, so you do not even need to import it.
