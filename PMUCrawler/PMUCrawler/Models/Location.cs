using System;
using System.Collections.Generic;
using System.Text;

namespace PMUCrawler.Models
{
    public class Location
    {
        public string Dungeon { get; set; }
        public string Floor { get; set; }
        public Location(string _Dungeon, string _Floor)
        {
            Dungeon = _Dungeon;
            Floor = _Floor;
        }
    }
}
