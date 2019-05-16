int	(*bdevsw[])()
{
	&nulldev,	&nulldev,	&rkstrategy,
	&tmopen,	&tmclose,	&tmstrategy,
	&nulldev,	&nulldev,	&rkstrategy
};

int	(*cdevsw[])()
{
	&klopen,   &klclose,   &klread,   &klwrite,   &klsgtty,
	&nulldev,  &nulldev,   &mmread,   &mmwrite,   &nodev,
	&nodev,   &nodev,   &nodev,   &nodev,   &nodev
};
