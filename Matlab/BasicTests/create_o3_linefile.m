copyfile( 'o3_some_lines.ac', 'tmp1.ac' );

!arts -r000 artscat2xml_no_mirror.arts

movefile( 'tmp2.xml', 'abs_lines_o3_afew.xml' );

delete( 'tmp1.ac' );
