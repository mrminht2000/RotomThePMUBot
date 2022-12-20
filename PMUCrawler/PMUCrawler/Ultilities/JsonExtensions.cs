using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace PMUCrawler.Ultilities
{
    public static class JsonExtensions
    {
        public static void SaveAsJson(object obj, string address)
        {
            using (StreamWriter file = File.CreateText(address))
            using (JsonTextWriter writer = new JsonTextWriter(file))
            {
                JsonSerializer serializer = new JsonSerializer();
                serializer.Serialize(file, obj);
            }
        }
    }
}
