using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trigger : MonoBehaviour
{
    Vector3[] Cord_massiv = new[]{
        new Vector3(10,10,10),
        new Vector3(-10,10,10),
        new Vector3(-10,10,-10),
        new Vector3(10,10,-10)
    };
    int i = 0;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    private void OnTriggerEnter(Collider other) {
        Debug.Log(transform.position);
        //transform.position = new Vector3(Random.Range(1,10),Random.Range(5,15),Random.Range(0,15));
        transform.position = Cord_massiv[i];
        i +=1;
        if (i>3) i = 0;

    }
}
