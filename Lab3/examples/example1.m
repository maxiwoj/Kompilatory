# special functions, initializations

a = -2+-3;

A = zeros(b + 3);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

E1 = [ 3, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;

A[1,3] = B[2,3] = 2;

D1 = -A+-B ; # add element-wise A with transpose of B
D2 -= A' ; # substract element-wise A with transpose of B
D3 *= A.*B'; # multiply element-wise A with transpose of B
D4 /= A./B' .+C./D ;


