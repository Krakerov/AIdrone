using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveDrone : MonoBehaviour
{
    private Rigidbody rbGO;
    public Transform Target;
    public float main_thrust = 2;
    public float P = 2f;
    public float I = 0.1f;
    public float i_error = 40f;
    public float D = 1f;
    float preErr = 0;
    public float SumPid;
    public float set = 6;
    public float SumThrust;
    public float angle;
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
        set = Target.position.y;
        
        i_error += (set - transform.position.y)*Time.deltaTime;
        
        if (Mathf.Abs(i_error)>30) i_error = i_error/Mathf.Abs(i_error) * 30;
        
        SumPid = (set - transform.position.y)*P + i_error*I +  (set - transform.position.y - preErr)/Time.deltaTime*D;
        if (SumPid < 0) SumPid = 0;
        preErr = set - transform.position.y;
        SumThrust = SumPid*main_thrust* (-Mathf.Cos(Mathf.Cos(angle))+2);
        if (SumThrust > 40) SumThrust = 40f;

        angle = Vector3.Angle(transform.up, new Vector3(0,1,0));
        rbGO.AddForce(transform.up * SumThrust);
        

    }
}
