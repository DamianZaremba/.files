cd ~;
if [ -d ".files/.git" ];
then
	cd ~/.files/;
	git pull;
	cd ~;
else
	git clone git://github.com/DamianZaremba/.files.git;
fi

if [ ! -d ".files/" ];
then
	echo "~/.files/ does not exist";
	exit 2;
fi

rsync -avr --exclude='update.sh' --exclude='README' ~/.files/* ~
rsync -avr --exclude='.git' ~/.files/.* ~
