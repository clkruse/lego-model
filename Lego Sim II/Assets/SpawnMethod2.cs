using UnityEngine;
using System.Collections;
using System.IO;
using System.Collections.Generic;

public class SpawnMethod2 : MonoBehaviour
{

    public HiResScreenShots captureHelper;

    public GameObject[] gameObjects;

    GameObject go;
    int currentIndex = 0;



    bool ready = true;
    public bool Enable;
    public int Repeat = 1;
    public string ImageLocation;
    public Vector3 scale = new Vector3(1, 1, 1);


    private void Start()
    {
        gameObjects = General.LoadResource();
    }


    public GameObject SpawnItem(GameObject a)
    {
        var igo = Instantiate(a);
        igo.transform.position = new Vector3(0, 0, 0);
        igo.transform.rotation = Random.rotation;
        igo.transform.parent = transform;
        igo.transform.localScale = scale;

        return igo;
    }

    int repeated = 0;
    public void Run()
    {
        if (currentIndex < gameObjects.Length)
        {
            Destroy(go);

            Debug.Log(currentIndex);
            go = SpawnItem(gameObjects[currentIndex]);


			captureHelper.TakeHiResShot(go.name.Replace("(Clone)", ""));

            if (repeated + 1 == Repeat)
            {
                currentIndex++;
                repeated = 0;
            }
            repeated++;
        }
        else
        {
            Enable = false;
            currentIndex = 0;
            repeated = 0;
            Debug.Log("Done.....!");
        }
    }

    private void Update()
    {
        if (!Enable)
            return;

        HiResScreenShots.path = ImageLocation;

        if (!captureHelper.processing)
        {
            Run();
            Debug.LogWarning("RUNNING");
        }
    }
}
