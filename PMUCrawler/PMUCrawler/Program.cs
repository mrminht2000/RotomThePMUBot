using HtmlAgilityPack;
using Newtonsoft.Json;
using PMUCrawler.Models;
using PMUCrawler.Ultilities;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace PMUCrawler
{
    class Program
    {
       
        static void Main(string[] args)
        {
            var res = PMUData.GetPokemonsInfo();

            JsonExtensions.SaveAsJson(res, "pkm.json");
        }
    }
}
