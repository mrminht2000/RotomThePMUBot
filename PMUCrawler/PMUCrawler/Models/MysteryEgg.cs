using System;
using System.Collections.Generic;
using System.Text;

namespace PMUCrawler.Models
{
    public class MysteryEgg
    {
        public string Name { get; set; }
        public List<EggLocation> Locations { get; set; }
    }

    public class EggLocation
    {
        public string Dungeon { get; set; }
        public string Floor { get; set; }
        public EggLocation(string _Dungeon, string _Floor)
        {
            Dungeon = _Dungeon;
            Floor = _Floor;
        }
    }
}
