using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

namespace PMUCrawler.Ultilities
{
    public static class StringExtension
    {
        public static string RemoveHtmlTag(this string input)
        {
            return Regex.Replace(input, "<.*?>", String.Empty);
        }

        public static string RemoveNewLineTag(this string input)
        {
            return Regex.Replace(input, "\n", String.Empty);
        }

        public static string InsertNewLine(this string input)
        {
            return Regex.Replace(input, "<p>", Environment.NewLine + "<p>");
        }

    }
}
