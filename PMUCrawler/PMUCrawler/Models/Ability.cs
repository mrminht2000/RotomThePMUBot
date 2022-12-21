using System;
using System.Collections.Generic;
using System.Text;

namespace PMUCrawler.Models
{
    public class Ability
    {
        public string Name { get; set; }
        public string ShortDescription { get; set; }
        public string Description { get; set; }

        public Ability(string _Name, string _ShortDescription, string _Description)
        {
            Name = _Name;
            ShortDescription = _ShortDescription;
            Description = _Description;
        }
    }
}
