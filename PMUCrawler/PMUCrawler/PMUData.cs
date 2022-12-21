using HtmlAgilityPack;
using PMUCrawler.Models;
using PMUCrawler.Ultilities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using static PMUCrawler.Models.Recruitment;

namespace PMUCrawler
{
    public static class PMUData
    {
        private const string BaseLink = "https://pokemonmysteryuniverse.fandom.com";
        private const string MysteryEggLink = "/wiki/Mystery_Eggs";
        private const string PokemonObtainGuide = "/wiki/Pokémon_Obtaining_Guide";
        private const string RecruitableGuide = "/wiki/Recruitable_Pokémon";
        private const string AbilityLink = "/wiki/Abilities";
        public static List<MysteryEgg> GetMysteryEggs()
        {
            var eggs = new List<MysteryEgg>();
            var _web = HtmlWebSingleton.GetInstance();
            HtmlDocument document = _web.Load(BaseLink + MysteryEggLink);
            var eggsTable = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/table[2]/tbody/tr").ToList();

            var tempEgg = new MysteryEgg
            {
                Name = "",
                Locations = new List<EggLocation>()
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
                        Locations = new List<EggLocation>()
                    };

                    var location = new EggLocation(detail[2].InnerText.RemoveNewLineTag(), detail[3].InnerText.RemoveNewLineTag());
                    tempEgg.Locations.Add(location);
                }
                else if (detail.Count() == 2)
                {
                    var location = new EggLocation(detail[0].InnerText.RemoveNewLineTag(), detail[1].InnerText.RemoveNewLineTag());
                    tempEgg.Locations.Add(location);
                }
            }
            return eggs;
        }

        public static List<Pokemon> GetPokemons()
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

        public static List<Recruitment> GetRecruitments()
        {
            var res = new List<Recruitment>();
            var _web = HtmlWebSingleton.GetInstance();
            HtmlDocument document = _web.Load(BaseLink + RecruitableGuide);

            var recuitTable = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/table[3]/tbody/tr").ToList();

            var tempRecruitment = new Recruitment
            {
                Name = "",
                Locations = new List<RecruitLocation>()
            };

            foreach (var item in recuitTable)
            {
                var detail = item.SelectNodes("td")?.ToList();
                if (detail == null)
                {
                    continue;
                }

                if (detail.Count() == 6)
                {
                    if (!tempRecruitment.Name.Equals(""))
                    {
                        res.Add(tempRecruitment);
                    }

                    tempRecruitment = new Recruitment
                    {
                        Name = detail[1].InnerText.RemoveNewLineTag(),
                        Locations = new List<RecruitLocation>()
                    };

                    var location = new RecruitLocation(detail[2].InnerText.RemoveNewLineTag(), detail[5].InnerText.RemoveNewLineTag(), detail[4].InnerText.RemoveNewLineTag(), detail[3].InnerText.RemoveNewLineTag());
                    tempRecruitment.Locations.Add(location);
                }
                else if (detail.Count() == 4)
                {
                    var location = new RecruitLocation(detail[0].InnerText.RemoveNewLineTag(), detail[3].InnerText.RemoveNewLineTag(), detail[2].InnerText.RemoveNewLineTag(), detail[1].InnerText.RemoveNewLineTag());
                    tempRecruitment.Locations.Add(location);
                }
            }

            if (!tempRecruitment.Name.Equals(""))
            {
                res.Add(tempRecruitment);
            }
            return res;
        }

        public static List<Ability> GetAbilities()
        {
            var res = new List<Ability>();
            var _web = HtmlWebSingleton.GetInstance();
            HtmlDocument document = _web.Load(BaseLink + AbilityLink);

            var abilityTable = document.DocumentNode.SelectNodes("//*[@id='mw-content-text']/div/ul").ToList();
    
            foreach (var abilityGroup in abilityTable)
            {
                var abilities = abilityGroup.SelectNodes("li").ToList();
                foreach (var ability in abilities)
                {
                    var tempAbility = new Ability(ability.InnerText.RemoveHtmlTag(), "Hasn't been described in PMU game!", "Unknown");
                    var link = ability.SelectSingleNode("a")?.Attributes["href"] ?? null;
                    if (link != null)
                    {
                        _web = HtmlWebSingleton.GetInstance();
                        var docAbility = _web.Load(BaseLink + link.Value);
                        var shortDescription = docAbility.DocumentNode.SelectSingleNode("//*[@id='mw-content-text']/div/p[1]");
                        var description = docAbility.DocumentNode.SelectSingleNode("//*[@id='mw-content-text']/div/p[2]") ?? null;
                        if (String.IsNullOrEmpty(description.InnerText.RemoveHtmlTag().RemoveNewLineTag()) || description == null)
                        {
                            description = docAbility.DocumentNode.SelectSingleNode("//*[@id='mw-content-text']/div/p[3]");
                        }
                        tempAbility.Description = description.InnerText.RemoveHtmlTag().RemoveNewLineTag().Replace("&#160;", " ");
                        tempAbility.ShortDescription = shortDescription.InnerText.RemoveHtmlTag().RemoveNewLineTag().Replace("&#160;", " ");
                    }
                    Console.WriteLine(tempAbility.Name + ": " +tempAbility.Description);
                    res.Add(tempAbility);
                }
            }
            return res;
        }

        private static List<Object> ReducePokemonObtainGuide(HtmlNode doc)
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
