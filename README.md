# Bitchute Video Add-On for Kodi

This is a free video add-on for [Kodi](https://kodi.tv/) which allows you to watch video from [Bitchute](https://www.bitchute.com/).

This repository was initialized with source code obtained from: https://github.com/celadoor/celadoor.github.io 

### Installation
Kodi expects the add-on to come in the form of a zip file. You can create a zip file of this repository after cloning, then import the file into Kodi.

Example of creating a zip file from the shell:

    # Run this from the repository's parent directory (not the repository's directory)
    zip -x .git/* -r plugin.video.bitchute.zip plugin.video.bitchute/*

If you do not know how to install an add-on from a zip file, you can [view the HOWTO](https://kodi.wiki/view/HOW-TO:Install_add-ons_from_zip_files) on the Kodi Wiki.

### License / Disclaimer
GPL v3. (See LICENSE.txt)

Use of Bitchute (including this add-on) is subject to their [Terms of Service](https://www.bitchute.com/policy/terms/) and other policies. If you do not agree with their policies, then you should not use this add-on.

As mentioned in LICENSE.txt, this software is provided "as-is" and without warranty. Some of the content found on Bitchute may be objectionable. You are responsible for your use of this software and the Bitchute service.

Use of this add-on is not officially supported by Bitchute. Since this add-on relies on parsing the HTML code of their website, it can stop working  if/when Bitchute makes updates to their web site's UI.

This software does not provide the full functionality of the Bitchute website. For example, there is no mechanism to log in and view your subscribed channels. As another example, there is no mechanism to flag content. Generally, if you want to use a feature that isn't available through this plugin, you can work around these limitations by visiting their website with a web browser.
