pySearchSelect=../pySearchSelect
function marks()
{
    lines=$(cat ~/.cdargs  | sed -e 's/^/\"/g' -e 's/$/\"/g')
    echo $lines
    # pySearchSelect shall be defined by your. I do it in my bashrc.
$pySearchSelect -f ~/.cdargsresult -l $lines
}
