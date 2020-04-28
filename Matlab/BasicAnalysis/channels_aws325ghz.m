% Returns limits for some AWS 325 GHz channels options
%
%    Limits for lower sideband returned
%
% FORMAT chs325 = channels_aws325ghz([option])
%
% OUT   chs325  Limits for lower sideband of ICI 325 GHz channels
% OPT   option  Option string.

% 2020-04-07 Patrick Eriksson

function chs325 = channels_aws325ghz(option)
%
if nargin == 0, option = '3'; end

switch option
  
  case '3'
    chs325 = 325.15e9 + [-8.00 -5.00;
                         -4.80 -2.30;
                         -2.20 -1.00 ] * 1e9;
  
  case '4'
    chs325 = 325.15e9 + [-8.00 -5.20;
                         -5.00 -3.10;
                         -3.00 -1.70;
                         -1.60 -0.80 ] * 1e9;
  
  otherwise
    error( 'Unknown option' );
end
