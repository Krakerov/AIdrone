using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveDrone : MonoBehaviour
{
    private Rigidbody rbGO;
    public Transform Target;
    public float main_thrust = 2;
    public float P = 6f;
    public float I = 0.5f;
    float i_error;
    public float D = 1.5f;
    float preErr = 0;
    float SumPid;
    public float set = 6;
    // Start is called before the first frame update
    void Start()
    {
        rbGO = gameObject.GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    void FixedUpdate() {
        i_error += (set - transform.position.y)*Time.deltaTime;
        SumPid = (set - transform.position.y)*P + i_error*I +  (set - transform.position.y - preErr)/Time.deltaTime*D;
        preErr = set - transform.position.y;
        rbGO.AddForce(transform.up * SumPid);

    }
}
