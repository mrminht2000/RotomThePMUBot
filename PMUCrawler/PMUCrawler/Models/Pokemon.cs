using System;
using System.Collections.Generic;
using System.Text;

namespace PMUCrawler.Models
{
    public class Pokemon
    {
        public string Name { get; set; }
        public List<Object> RawInfo { get; set; }

        public Pokemon (string name)
        {
            Name = name;
            RawInfo = new List<Object>();
        }
    }
}
