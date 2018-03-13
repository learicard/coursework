function word_indices = processEmail(email_contents)
    % PROCESSEMAIL preprocesses a the body of an email and
    % returns a list of word_indices
    % word_indices = PROCESSEMAIL(email_contents) preprocesses
    % the body of an email and returns a list of indices of the
    % words contained in the email.

    vocabList = getVocabList();
    word_indices = [];

    % Uncomment the following lines if you are working with raw emails with the
    % full headers
    % hdrstart = strfind(email_contents, ([char(10) char(10)]));
    % email_contents = email_contents(hdrstart(1):end);

    email_contents = lower(email_contents);
    email_contents = regexprep(email_contents, '<[^<>]+>', ' '); % strip HTML
    email_contents = regexprep(email_contents, '[0-9]+', 'number');
    email_contents = regexprep(email_contents, '(http|https)://[^\s]*', 'httpaddr');
    email_contents = regexprep(email_contents, '[^\s]+@[^\s]+', 'emailaddr');
    email_contents = regexprep(email_contents, '[$]+', 'dollar');

    fprintf('\n==== Processed Email ====\n\n');

    l = 0;
    while ~isempty(email_contents)

        % Tokenize and also get rid of any punctuation
        [str, email_contents] = strtok(email_contents, [' @$/#.-:&*+=[]?!(){},''">_<;%' char(10) char(13)]);

        % Remove any non alphanumeric characters
        str = regexprep(str, '[^a-zA-Z0-9]', '');

        % Stem the word
        try str = porterStemmer(strtrim(str));
        catch str = '';
            continue;
        end;

        % Skip the word if it is too short
        if length(str) < 1
            continue;
        end


        idx = find(ismember(vocabList, str));
        if isempty(idx) ~= 1;
            word_indices = [word_indices; idx];
        end

        % Print to screen, ensuring that the output lines are not too long
        if (l + length(str) + 1) > 78
            fprintf('\n');
            l = 0;
        end
        fprintf('%s ', str);
        l = l + length(str) + 1;
    end
end
