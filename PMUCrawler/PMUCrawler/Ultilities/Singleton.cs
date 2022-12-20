using HtmlAgilityPack;
using PMUCrawler.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;

namespace PMUCrawler.Ultilities
{
    public class MysteryEggWindowSingleton
    {
        private static MysteryEgg _instance;

        // Constructor is 'protected'
        protected MysteryEggWindowSingleton()
        {
        }

        public static MysteryEgg GetInstance()
        {
            // Uses lazy initialization.
            // Note: this is not thread safe.
            if (_instance == null)
            {
                _instance = new MysteryEgg();
            }

            return _instance;
        }
    }

    public class HtmlWebSingleton
    {
        private static HtmlWeb _instance;

        // Constructor is 'protected'
        protected HtmlWebSingleton()
        {
        }

        public static HtmlWeb GetInstance()
        {
            // Uses lazy initialization.
            // Note: this is not thread safe.
            if (_instance == null)
            {
                _instance = new HtmlWeb();
            }

            return _instance;
        }
    }
}
