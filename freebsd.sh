#!/bin/bash

STAGEDIR=/tmp/stage_hvdaemon

rm -rf $STAGEDIR
mkdir $STAGEDIR

cat >> ${STAGEDIR}/+POST_INSTALL <<EOF
ln -s /usr/local/lib/python2.7/site-packages/hvdaemon
EOF

cat >> ${STAGEDIR}/+MANIFEST <<EOF
name: hvdaemon
version: "1.0_0"
origin: sysutils/hvdaemon
comment: "Hyper-V Daemon"
desc: "system configuration via Hyper-V Daemon"
maintainer: zegrep@gmail.com
www:
prefix: /
EOF

echo "deps: {" >> ${STAGEDIR}/+MANIFEST
pkg query '  %n: { version: "%v", origin: %o }' py27-pyinotify >> ${STAGEDIR}+MANIFEST
echo "}" >> ${STAGEDIR}/+MANIFEST

PACKAGEDIR=${STAGEDIR}/usr/local/lib/python2.7/site-packages/hvdaemon
mkdir -p ${PACKAGEDIR}
cp ./hvdaemon/*.py ${PACKAGEDIR}
echo "# hello world" > ${STAGEDIR}/usr/local/etc/my.conf
for file in ${PACKAGEDIR}/; do
    echo "${PACKAGEDIR}/${file}" >> ${STAGEDIR}/plist
done
