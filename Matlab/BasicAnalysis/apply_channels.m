function weighted = apply_channels(f_mono,monochrom,channels)

n        = size( channels, 1 );
weighted = zeros( size(monochrom,1), n );

for c = 1 : n
  ind = find( f_mono >= channels(c,1) & f_mono <= channels(c,2) ); 
  weighted(:,c) = mean( monochrom(:,ind), 2 );
end
