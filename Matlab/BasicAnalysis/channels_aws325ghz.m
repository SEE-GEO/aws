function chs325 = channels_aws325ghz(only3)
%
if nargin == 0, only3 = false; end


if only3
  chs325 = 325.15e9 + [-9.00 -5.00;
                       -4.70 -2.30;
                       -2.30 -0.80 ] * 1e9;
else    
  chs325 = 325.15e9 + [-9.00 -6.00;
                       -6.00 -3.60;
                       -3.60 -1.80;
                       -1.80 -0.80 ] * 1e9;
end
