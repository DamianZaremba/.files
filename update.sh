cd ~;
if [ -d ".files/.git" ];
then
	cd ~/.files/;
	git pull;
	git submodule update
else
	git clone git://github.com/DamianZaremba/.files.git;
	cd ~/.files/
	git submodule update --init
fi
cd ~

if [ ! -d ".files/" ];
then
	echo "~/.files/ does not exist";
	exit 2;
fi

rsync -avr --exclude='update.sh' --exclude='README' ~/.files/* ~
rsync -avr --exclude='.git' --exclude='.gitmodules' ~/.files/.* ~
