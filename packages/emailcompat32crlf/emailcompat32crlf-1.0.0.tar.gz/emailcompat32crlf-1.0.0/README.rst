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

Why patch the standard lib, instead of fixing your own code?
------------------------------------------------------------

Because to fix your own code, you'd have to ensure to override the default
policy in every single instantiation of every ``Message`` or ``MIMEText`` or any
of the other constructors which default to the ``compat32`` policy
without carriage returns.

Instead, you now can simply add ``emailcompat32crlf`` to your project. Done.
