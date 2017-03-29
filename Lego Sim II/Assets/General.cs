using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEngine;

public static class General
{
    public static GameObject[] LoadResource()
    {

        var go = (GameObject)Resources.Load("175");
        var gameObjects = new GameObject[1];
        gameObjects[0] = go;
        //var objs = Resources.LoadAll("Assets\\Resources"); 
        //for (int i = 0; i < objs.Length; i++)
        //{
        //    gameObjects = new GameObject[objs.Length];
        //    gameObjects[i] = (GameObject)objs[i];
        //}


        FileInfo[] fileInfo = new DirectoryInfo(Application.dataPath + "/Resources").GetFiles();// .GetFiles(Application.dataPath);//.GetFiles("*.*", SearchOption.AllDirectories);

        List<string> fileNames = new List<string>();

        foreach (FileInfo file in fileInfo)
        {
            // file name check
            if (file.Name == "something")
            {
            }
            // file extension check
            if (file.Extension == ".3ds")
            {
                fileNames.Add(file.Name);
            }
            // etc.
        }

        gameObjects = new GameObject[fileNames.Count];
        for (int i = 0; i < fileNames.Count; i++)
        {
            var x = (GameObject)Resources.Load(fileNames[i].Remove(fileNames[i].Length - 4, 4));
            gameObjects[i] = x;
        }

        return gameObjects;
    }

}
