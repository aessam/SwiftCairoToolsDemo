var crypto = require('crypto');
var fsevents = require('fsevents');
var fs = require('fs');
const { exec } = require('child_process');

function shahash(str) {
	var hash = crypto.createHash('sha1');
	hash.setEncoding('hex');
	hash.write(str);
	hash.end();
	return hash.read();
}

function checkAndShow(path) {
	if (path.endsWith('ToolsDemo/ImportantFile.swift')) {
		if (shahash(fs.readFileSync(path, 'utf8')) !== '08bc163f939afbecc82915ce63caf87f105a5d9d') {
			exec('osascript -e \'display notification "الملف مكتوب فيه متعدلوش، يعني نولع في الجهاز علشان تبطل" with title "أنا هقول للتيم ليدر على فكرة"\'');
		}
	}
}
var watcher = fsevents(__dirname);
watcher.on('change', checkAndShow);
watcher.start();
setTimeout(function(t) {console.log(watcher.stop())}, 15000)
