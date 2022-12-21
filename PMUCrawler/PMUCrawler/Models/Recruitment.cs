using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

namespace PMUCrawler.Models
{
    public class Recruitment
    {
        public string Name { get; set; }
        public List<RecruitLocation> Locations { get; set; }
        public class RecruitLocation
        {
            public string Dungeon { get; set; }
            public string Floor { get; set; }
            public double RecruitRate { get; set; }
            public string Time { get; set; }
            public RecruitLocation(string _Dungeon, string _Floor, string _Time, string _RecruitRate)
            {
                Dungeon = _Dungeon;
                Floor = _Floor;
                Time = _Time;
                RecruitRate = Double.Parse(Regex.Replace(_RecruitRate, "%", String.Empty));
            }
        }
    }
}
