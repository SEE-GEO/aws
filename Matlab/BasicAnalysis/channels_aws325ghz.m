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
    chs325 = 325.15e9 + [-9.00 -5.00;
                         -4.70 -2.30;
                         -2.30 -0.80 ] * 1e9;
  
  case '4'
    chs325 = 325.15e9 + [-9.00 -6.00;
                         -6.00 -3.60;
                         -3.60 -1.80;
                         -1.80 -0.80 ] * 1e9;
  
  otherwise
    error( 'Unknown option' );
end
