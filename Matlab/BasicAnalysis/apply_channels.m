% FORMAT  weighted = apply_channels(f_mono,monochrom,channels)
%
% OUT  weighted   Channel weighted values
% IN   f_mono     Monochromatic frequency grid
%      monochrom  Monochromatic values (nf,nx)  
%      channels   As return by eg. *channels_fixed*

% 2020-04-07 Patrick Eriksson

function weighted = apply_channels(f_mono,monochrom,channels)

n        = size( channels, 1 );
weighted = zeros( n, size(monochrom,2) );

for c = 1 : n
  ind = find( f_mono >= channels(c,1) & f_mono <= channels(c,2) ); 
  weighted(c,:) = mean( monochrom(ind,:), 1 );
end
