clear all;
close all;

er = imread('ertka.bmp');
tab1 = [1,1,1
       0,0,0
       0 0 0];
tab2 = [0 0 1
        0 0 1
        0 0 1];
tab3 = [0 0 0
        0 0 0
        1 1 1];
tab4 = [1 0 0
        1 0 0
        1 0 0];

% tab1 = [0,1,0
%        0,0,0
%        0 0 0];
% tab2 = [0 0 0
%         0 0 1
%         0 0 0];
% tab3 = [0 0 0
%         0 0 0
%         0 1 0];
% tab4 = [0 0 0
%         1 0 0
%         0 0 0];






er_ = er(:,:,1);





er1 = er_;
er2 = er1;
er3 = er1;
er4 = er1;

masked1 = zeros(3,3);
masked2 = masked1;
masked3 = masked1;
masked4 = masked1;

for y = 1:size(er_,1)-2
    for x = 1:size(er_,2)-2
        for i = y:y+2
            for j = x:x+2
                masked1(i-y+1,j-x+1) = er_(i,j);
            end
        end
        masked2 = masked1;
        masked3 = masked1;
        masked4 = masked1;

        masked1 = masked1.*tab1;
        masked2 = masked2.*tab2;
        masked3 = masked3.*tab3;
        masked4 = masked4.*tab4;
        

        if(masked1(1,1)==masked1(1,2) && masked1(1,3)==masked1(1,2))
            er1(y,x+1) = 255;
        end
        if(masked2(1,3)==masked2(2,3) && masked2(3,3)==masked2(2,3))
            er2(y+1,x+2) = 255;
        end
        if(masked3(3,3)==masked3(3,2) && masked3(3,1)==masked3(3,2))
            er3(y+2,x+1) = 255;
        end
        if(masked4(1,1)==masked4(2,1) && masked4(3,1)==masked4(2,1))
            er4(y+1,x) = 255;
        end


%         if(masked1(1,1)==masked1(1,2))
%             er1(y,x) = 255;
%         end
%         if(masked1(1,3)==masked1(1,2))
%             er1(y,x+2) = 255;
%         end
% 
%         if(masked2(1,3)==masked2(2,3))
%             er2(y,x+2) = 255;
%         end
%         if(masked2(3,3)==masked2(2,3))
%             er2(y+2,x+2) = 255;
%         end
% 
%         if(masked3(3,1)==masked3(3,2))
%             er3(y+2,x) = 255;
%         end
%         if(masked3(3,3)==masked3(3,2))
%             er3(y+2,x+2) = 255;
%         end
% 
%         if(masked4(1,1)==masked4(2,1))
%             er4(y,x) = 255;
%         end
%         if(masked4(1,3)==masked4(2,1))
%             er4(y+2,x) = 255;
%         end
    end
end


for y = 1:size(er_,1)
    for x = 1:size(er_,2)
        if(er1(y,x)==255)
            er1(y,x) = 0;
        else
            er1(y,x) = 255;
        end

        if(er2(y,x)==255)
            er2(y,x) = 0;
        else
            er2(y,x) = 255;
        end

        if(er3(y,x)==255)
            er3(y,x) = 0;
        else
            er3(y,x) = 255;
        end

        if(er4(y,x)==255)
            er4(y,x) = 0;
        else
            er4(y,x) = 255;
        end
    end
end





er_ = er_ + er1 + er2 + er3 +er4;

subplot(3,2,1)
    imshow(er)
subplot(3,2,2)
    imshow(er1)
subplot(3,2,3)
    imshow(er2)
subplot(3,2,4)
    imshow(er3)
subplot(3,2,5)
    imshow(er4)
subplot(3,2,6)
    imshow(er_)