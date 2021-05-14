def share(title, text):
    from kivy import platform

    if platform == 'android':
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(text)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String(title))
        PythonActivity.mActivity.startActivity(chooser)
