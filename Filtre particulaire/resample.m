function [ x_return ] = resample( xt, wt, N_part )

x_return = zeros(N_part,1);

for i = 1:N_part
    u = rand(1);
    j=1;
    while ( sum( wt(1:j)) < u)
        j=j+1;
    end
       
    x_return(i) = xt(j);

end

