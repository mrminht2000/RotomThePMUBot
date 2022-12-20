using HtmlAgilityPack;
using PMUCrawler.Models;
using PMUCrawler.Ultilities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PMUCrawler
{
    public static class PMUData
    {
        private const string BaseLink = "https://pokemonmysteryuniverse.fandom.com/wiki/";
        private const string MysteryEggLink = "Mystery_Eggs";
        private const string PokemonObtainGuide = "Pokémon_Obtaining_Guide";
        public static List<MysteryEgg> GetMysteryEggInfo()
        {
            var eggs = new List<MysteryEgg>();
            var _web = HtmlWebSingleton.GetInstance();
            HtmlDocument document = _web.Load(BaseLink + MysteryEggLink);
            var eggsTable = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/table[2]/tbody/tr").ToList();

            var tempEgg = new MysteryEgg
            {
                Name = "",
                Locations = new List<Location>()
            };

            foreach (var item in eggsTable)
            {
                var detail = item.SelectNodes("td")?.ToList();
                if (detail == null)
                {
                    continue;
                }

                if (detail.Count() == 4)
                {
                    if (!tempEgg.Name.Equals(""))
                    {
                        eggs.Add(tempEgg);
                    }

                    tempEgg = new MysteryEgg
                    {
                        Name = detail[1].InnerText.RemoveNewLineTag(),
                        Locations = new List<Location>()
                    };

                    var location = new Location(detail[2].InnerText.RemoveNewLineTag(), detail[3].InnerText.RemoveNewLineTag());
                    tempEgg.Locations.Add(location);
                }
                else if (detail.Count() == 2)
                {
                    var location = new Location(detail[0].InnerText.RemoveNewLineTag(), detail[1].InnerText.RemoveNewLineTag());
                    tempEgg.Locations.Add(location);
                }
            }
            return eggs;
        }

        public static List<Pokemon> GetPokemonsInfo ()
        {
            var res = new List<Pokemon>();
            var _web = HtmlWebSingleton.GetInstance();
            HtmlDocument document = _web.Load(BaseLink + PokemonObtainGuide);

            for (int i = 2; i <= 9; i++)
            {
                var pokemonTable = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/table[" + i.ToString() + "]/tbody/tr").ToList();
                
                foreach(var item in pokemonTable)
                {
                    var detail = item.SelectNodes("td")?.ToList();
                    if (detail == null || String.IsNullOrEmpty(detail[1].InnerText))
                    {
                        continue;
                    }
                    var pkm = new Pokemon(detail[1].InnerText.RemoveNewLineTag());
                    pkm.RawInfo = ReducePokemonObtainGuide(detail[2]);

                    var note = item.SelectNodes("td/dl/dd")?.ToList();
                    if (note != null && note.Count != 0)
                    {
                        pkm.Note = note[0].InnerText.RemoveHtmlTag().RemoveNewLineTag().Replace("SRSecret Room", " Secret Room").Replace("HHidden", " Hidden");
                    }
                    res.Add(pkm);
                }
            }

            return res;
        }

        public static List<Object> ReducePokemonObtainGuide(HtmlNode doc)
        {
            var detail = doc.SelectNodes("ul/li")?.ToList();
            var res = new List<Object>();
            foreach (var item in detail)
            {
                var tempString = item.InnerText.RemoveHtmlTag().Split('\n').FirstOrDefault();

                var ulInside = item.SelectNodes("ul/li")?.ToList();
                if (ulInside != null)
                {
                    var changeTypeInfo = new Dictionary<string, List<string>>();
                    changeTypeInfo.Add(tempString, new List<string>());
                    foreach (var item2 in ulInside)
                    {
                        changeTypeInfo[tempString].Add(item2.InnerText.RemoveHtmlTag().RemoveNewLineTag().Replace("SRSecret Room", " Secret Room").Replace("HHidden", " Hidden"));
                    }

                    res.Add(changeTypeInfo);
                } else
                {
                    res.Add(tempString.Replace("SRSecret Room", " Secret Room").Replace("HHidden", " Hidden"));
                }
                Console.WriteLine(tempString);
            }

            return res;
        }
    }
}
