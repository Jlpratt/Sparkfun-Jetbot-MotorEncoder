finaltable = zeros(155,3);
for j = 1:155
    clear rightindex leftindex data m angv fil i fileName left right rightcount leftcount i
    fil=255-(j-1);
    fileName = sprintf('JetbotData/JetbotProject-main/%d.csv',fil);
    data = readtable(fileName);
    m = table2array(data(:,1));
%data = table2array(data);
    m = cell2mat(m);
    angv = table2array(data(:,2));
    %angv = cell2mat(angv);
    leftindex = sum(m=='l');
    rightindex = sum(m=='r');
    left = zeros(leftindex,1);
    right = zeros (rightindex,1);
    rightcount = 0;
    leftcount = 0;
   for i= 1:length(angv)
        if m(i,1) == 'r'
            rightcount = rightcount+1;
            right(rightcount)=angv(i);
            
        elseif m(i,1) == 'l'
            leftcount = leftcount+1;
            left(leftcount) = angv(i);
        end
   end
   right = right;%*360;
   left=left;%*360;
    %[r,trf] = rmoutliers(right,'quartiles');
    %[l,tlf] = rmoutliers(left, 'quartiles');
    %plot(left)
    %hold on
    %[r,trf] = rmoutliers(right,'quartiles');
    %[l,tlf] = rmoutliers(left, 'quartiles');
    xval = 1:length(left);
    
    %hold off
avgl = mean(left(5:end));
avgr = mean(right(5:end));
fprintf('%d\n',fil)    
fprintf('%d\n',mean(left(5:end)));
fprintf('%d\n',mean(right(5:end)));
finaltable(j,1) = fil;
finaltable(j,2) = avgl;
finaltable(j,3) = avgr;
%scatter(xval,avgl);
end