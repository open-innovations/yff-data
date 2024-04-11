#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
binmode(STDOUT, ":utf8");

my %colours = (
	'black'=>"\033[0;30m",
	'red'=>"\033[0;31m",
	'green'=>"\033[0;32m",
	'yellow'=>"\033[0;33m",
	'blue'=>"\033[0;34m",
	'magenta'=>"\033[0;35m",
	'cyan'=>"\033[0;36m",
	'white'=>"\033[0;37m",
	'none'=>"\033[0m"
);


# Run the grouping 
# buildCSV(inputfile,outputfile,configuration)
buildCSV("working/upstream/oecd_lfs_by_sex_and_age.csv","src/areas/maps/international/_data/view/oecd_lfs_grouped.csv",{
	'groupby'=>[
		{'value'=>'measure'},
		{'value'=>'sex'},
		{'value'=>'age'},
	],
	'keep'=>['country','units'],
	'col'=>{'value'=>'time_period'},
	'row'=>{'value'=>'country_code','valid'=>sub {  my($v) = shift; return (length($v) eq 3); }},
	'value'=>{'value'=>'value','format'=>sub { my $v = shift; return sprintf("%0.2f",$v); }}
});







#############################

# A function to flatten a hash.
# If a "maxdepth" is provided, we'll only go to that depth.
# Returns keys concatenated with "->".
sub flatten_hash {
    my %output = %{shift @_};
    my %args = @_;
	if(!defined($args{'depth'})){ $args{'depth'} = 0; }
    while (my ($key, $value) = each(%{$args{original_hash}})) {
        my @data_address = defined($args{keys_list}) ? @{$args{keys_list}} : ();
		
		if(defined($args{'maxdepth'})){
			if($args{'depth'} < $args{'maxdepth'}){

				push(@data_address, $key);

				if(ref($value) eq 'HASH') {
					%output = flatten_hash(\%output, original_hash => $value, keys_list => \@data_address, depth => $args{'depth'}+1, maxdepth => $args{'maxdepth'});
				}else{
					my $addr = join('->', @data_address);
					$output{$addr} = $value;
				}
			}else{
				my $addr = join('->', @data_address);
				$output{$addr} = $args{original_hash};
			}
		}else{
			push(@data_address, $key);

			if(ref($value) eq 'HASH') {
				%output = flatten_hash(\%output, original_hash => $value, keys_list => \@data_address, depth => $args{'depth'}+1, maxdepth => $args{'maxdepth'});
			}else{
				my $addr = join('->', @data_address);
				$output{$addr} = $value;
			}
			
		}
    }
    return %output;
}

# Get a property using e.g. "a->b->c"
sub getProperty {
	my $p = shift;
	my $d = shift;
	my @bits = split(/\-\>/,$p);
	my $n = @bits;
	my ($out,$key);
	if($n > 1){
		$key = shift(@bits);
		return getProperty(join("->",@bits),$d->{$key});
	}else{
		return $d->{$p};
	}
}

# Build the CSV
sub buildCSV {
	my ($file,$ofile,$conf) = @_;

	my (@csvrows,@rows,@cols,@datacols,$i,$p,$n,$r,$c,$k,$data,$rowlist,$collist,$row,%out,@headers,$head,$body,$spacer,@parts,@csvrow,@keep);

	@csvrows = LoadCSV($file);

	$data = {'extra'=>{}};
	$rowlist = {};
	$collist = {};

	$conf->{'row'}{'list'} = $rowlist;
	$conf->{'col'}{'list'} = $collist;


	# Loop over all the rows in the CSV
	for($i = 0; $i < @csvrows; $i++){
		$data = groupData($conf,$csvrows[$i],$data);
		$row = $csvrows[$i]->{$conf->{'row'}{'value'}};
		$data->{'extra'}{$row} = {};
		for($k = 0; $k < @{$conf->{'keep'}}; $k++){
			if(!defined($data->{'extra'}{$row}{$conf->{'keep'}[$k]})){
				$data->{'extra'}{$row}{$conf->{'keep'}[$k]} = $csvrows[$i]->{$conf->{'keep'}[$k]};
			}
		}
	}

	@rows = sort(keys(%{$conf->{'row'}{'list'}}));
	@cols = sort(keys(%{$conf->{'col'}{'list'}}));

	$n = @{$conf->{'groupby'}};

	%out = flatten_hash({}, original_hash => $data->{'data'}, 'maxdepth'=>$n+1);
	@datacols = sort(keys(%out));


	$body = "";
	$head = "";
	$spacer = "";
	@keep = @{$conf->{'keep'}};
	@headers = ();
	for($c = 0; $c < @datacols; $c++){
		@parts = split(/->/,$datacols[$c]);		
		for($p = 0; $p < @parts; $p++){
			push(@{$headers[$p]},$parts[$p]);
		}
	}
	# Add the row name as the first column header
	$head .= $conf->{'row'}{'value'};
	$spacer .= "---";
	for($i = 0; $i < @headers; $i++){
		
		# Add any "keep" columns
		if(@keep > 0){
			if($i == 0){
				$head .= ",".join(",",@keep);
				$spacer .= (",---" x @keep);
			}else{
				$head .= ("," x @keep);
			}
		}

		$head .= ",".join(",",@{$headers[$i]})."\n";
		
		
		if($i==0){
			$spacer .= (",---" x @{$headers[$i]})."\n";
		}
	}

	$body = "";
	for($r = 0; $r < @rows; $r++){
		$body .= $rows[$r];

		# Add any "keep" columns
		if(@keep > 0){
			for($k = 0; $k < @keep; $k++){
				$body .= ",".($data->{'extra'}{$rows[$r]}{$keep[$k]} =~ /\,/ ? "\"$data->{'extra'}{$rows[$r]}{$keep[$k]}\"" : $data->{'extra'}{$rows[$r]}{$keep[$k]});
			}
		}

		@csvrow = ();
		for($c = 0; $c < @datacols; $c++){
			push(@csvrow,getProperty($datacols[$c]."->".$rows[$r],$data->{'data'})||"");
		}
		$body .= ",".join(",",@csvrow)."\n";
	}
	
	msg("Saving to <cyan>$ofile<none>\n");
	open(FILE,">",$ofile);
	print FILE $head.$spacer.$body;
	close(FILE);
	return $head.$spacer.$body;
}

sub groupData {
	my ($conf,$row,$data) = @_;
	my ($code,$ok,$g,$v,$yy,@gs,$d);
	$ok = 1;

	if($ok){

		if(!defined($data->{'data'})){ $data->{'data'} = {}; }
		$d = $data->{'data'};
		
		@gs = @{$conf->{'groupby'}};
		# Add the col/row groupings
		push(@gs,$conf->{'col'});
		push(@gs,$conf->{'row'});
		for($g = 0; $g < @gs; $g++){
			$v = $row->{$gs[$g]->{'value'}};
			
			if(ref($gs[$g]->{'valid'}) eq "CODE"){
				$ok = ($gs[$g]->{'valid'}($v));
			}
			if($ok){
				if($gs[$g]->{'list'} && ref($gs[$g]->{'list'}) eq "HASH"){
					$gs[$g]->{'list'}{$v} = 1;
				}

				if(!defined($d->{$v})){
					if($g == @gs-1){
						$d->{$v} = $row->{$conf->{'value'}{'value'}};
						if(ref($conf->{'value'}{'format'}) eq "CODE"){
							$d->{$v} = $conf->{'value'}{'format'}($d->{$v});
						}
					}else{
						$d->{$v} = {};
					}
				}
				$d = $d->{$v};
			}else{
				last;
			}
		}
	}
	
	return ($data);
}


sub msg {
	my $str = $_[0];
	my $dest = $_[1]||"STDOUT";
	foreach my $c (keys(%colours)){ $str =~ s/\< ?$c ?\>/$colours{$c}/g; }
	if($dest eq "STDERR"){
		print STDERR $str;
	}else{
		print STDOUT $str;
	}
}

sub error {
	my $str = $_[0];
	$str =~ s/(^[\t\s]*)/$1<red>ERROR:<none> /;
	msg($str,"STDERR");
	exit;
}

sub warning {
	my $str = $_[0];
	$str =~ s/(^[\t\s]*)/$1$colours{'yellow'}WARNING:$colours{'none'} /;
	msg($str,"STDERR");
}

sub LoadCSV {
	my $file = shift;
	my $col = shift;

	my (@lines,$str,@rows,@cols,@header,$r,$c,@features,$data,$key,$k,$f);

	msg("Processing CSV from <cyan>$file<none>\n");
	open(FILE,"<:utf8",$file);
	@lines = <FILE>;
	close(FILE);
	$str = join("",@lines);
	@rows = split(/[\r\n]+/,$str);

	for($r = 0; $r < @rows; $r++){
		@cols = split(/,(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))/,$rows[$r]);
		for($c = 0; $c < @cols; $c++){
			$cols[$c] =~ s/(^\"|\"$)//g;
		}
		if($r < 1){
			# Header
			if(!@header){
				@header = @cols;
			}else{
				for($c = 0; $c < @cols; $c++){
					$header[$c] .= "\n".$cols[$c];
				}
			}
		}else{
			$data = {};
			for($c = 0; $c < @cols; $c++){
				$data->{$header[$c]} = $cols[$c];
			}
			push(@features,$data);
		}
	}
	if($col){
		$data = {};
		for($r = 0; $r < @features; $r++){
			$data->{$features[$r]->{$col}} = $features[$r];
		}
		return $data;
	}else{
		return @features;
	}
}
