using UnityEngine;
using System.Collections;

public class SpawnManager : MonoBehaviour
{
    public HiResScreenShots captureHelper;

    public GameObject[] gameObjects;

    GameObject go;
    Rigidbody rb;
    bool readyToSpawn = true;
    bool readyToCapture;
    int currentIndex = 0;


    bool ready = true;

    public bool Enable;
    public int Repeat = 1;
    public string ImageLocation;
	public string brickName;
    public Vector3 scale = new Vector3(1, 1, 1);
    public int speed = 1; 
    private void Start()
    {
        gameObjects = General.LoadResource();
    }

    public GameObject SpawnItem(GameObject a)
    {

        var igo = Instantiate(a);

        igo.transform.rotation = Random.rotation;
        igo.transform.parent = transform;
        igo.transform.localPosition = new Vector3(0, 0, 0);
        igo.transform.localScale = scale;
        igo.AddComponent<MeshCollider>();

        var rigidbody = igo.AddComponent<Rigidbody>();
		//rb.velocity = new Vector3 (1, 1, 1);
         
        foreach (Transform child in igo.transform)
        {
            var material = child.GetComponent<Renderer>().material;
            if (material != null)
            {
                if (material.name == "Default-Material (Instance)")
                    Destroy(child.gameObject);
                else
                {
                    child.gameObject.AddComponent<MeshCollider>().convex = true;
                }
            } 
        }
      

        return igo;
    }





    int repeated = 0;
    public void Run()
    {
        if (currentIndex < gameObjects.Length)
        {
            if (readyToSpawn)
            {
                Destroy(go);
  
                go = SpawnItem(gameObjects[currentIndex]);
                rb = go.GetComponent<Rigidbody>();
                rb.velocity = new Vector3(1, 1, 1);
				brickName = rb.name;
				Debug.Log(string.Format(brickName));
                readyToSpawn = false;
                if (repeated + 1 == Repeat)
                {
                    currentIndex++;
                    repeated = 0;
                }
                repeated++;
            }
        }
        else
        {
            Enable = false;
            currentIndex = 0;
            repeated = 0;
            Debug.Log("Done.....!");
        }
    }


    int speedOldValue = 0;
    private void Update()
    {
        if (!Enable)
            return;
        if (speedOldValue != speed)
            Time.timeScale = speedOldValue = speed;

        HiResScreenShots.path = ImageLocation;


        if (go != null && rb != null)
        {
            //Camera.main.transform.LookAt(go.transform);

			if (rb.velocity.x < 0.000001)
            {
				for(int i = 0; i < 100; i++)
				{
				}

              //Stationary
				captureHelper.TakeHiResShot(go.name.Replace("(Clone)", ""));
                rb = null;
                readyToSpawn = true;
            }
        }
        else
        {
            if (!captureHelper.processing)
                Run();
        }

    }


}
