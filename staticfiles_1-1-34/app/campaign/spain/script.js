let router = new Navigo(null, true, '#!');
let app = document.getElementById('app');

let resObj = null;
let payment_res = null;

router.on({
    "/": function(){
     app.innerHTML = `
     <div class="form">
     <form id="dataForm">
     <div class="text3x bold">ROBERTS CANADA SOCCER ACADEMY</div>
     <div class="sub2xtext">2022 Spain Id Camp Registration Form</div>
     
     <div class="input-field">
     <input type="text" name="name" id="name" required/>
     <label for="name">Name</label>
     </div>
     
  <div>
     Gender: 
      <label>
        <input value="MALE" name="gender" type="radio" checked required/>
        <span>Male</span>
      </label>
  
      <label>
        <input value="FEMALE" name="gender" type="radio" required/>
        <span>Female</span>
      </label>
  </div>

    <input type="text" name="dob" placeholder="Date of birth" class="datepicker" required>
    
    <div class="input-field">
    <input value="dshsjdh" type="text" name="parent_names" id="parents_name" required/>
    <label for="parents_name">Parents' Name</label>
    </div>

    <div class="input-field">
    <input type="text" name="address" id="address" required/>
    <label for="address">Address(include city ans postal code)</label>
    </div>

    <div class="input-field">
    <input type="number" name="phone" id="phone" required/>
    <label for="phone">Phone</label>
    </div>

    <div class="input-field">
    <input type="email" name="parents_email" id="parents_email" required/>
    <label for="parents_email">Parents's Email</label>
    </div>

    <div class="input-field">
    <input type="email" name="player_email" id="player_email" required/>
    <label for="player_email">Player Email</label>
    </div>

    <div class="input-field">
    <input value="1234" type="number" name="healt_card_num" id="healt_card_num" required/>
    <label for="healt_card_num">Health Card Number</label>
    </div>

    <div class="input-field">
    <input value="dshsjdh" type="text" name="medications" id="medications" required/>
    <label for="medications">Medications</label>
    </div>

    <div class="input-field">
    <input value="dshsjdh" type="text" name="allergies" id="allergies" required/>
    <label for="allergies">Allergies</label>
    </div>

    <div class="input-field">
    <input value="dshsjdh" type="text" name="injuries" id="injuries"required required/>
    <label for="injuries">Injuries</label>
    </div>

    <div class="input-field">
    <input value="13235" type="number" name="emerg_contact" id="emerg_contact" required/>
    <label for="emerg_contact">Emergency Contact</label>
    </div>

    <div class="input-field">
    <select name="reg_fees" required>
      <option value="-1" dispi_3L4hT6JFEKrz679r1Cq0kFfU_secret_iADet4WZcnqwJZWQtzi0wd4xabled selected>Registration Fees:</option>
      <option value="8ff49c60c356471285a5411d24964534">Mississauga ID Camp: $350.00 (U15-U22)</option>
      <option value="7a4c01f13bb84f57a0d6281c5eba7794">Mississauga ID Camp: $250.00 (U10-U14)</option>
      <option value="2">Cambridge ID Camp: $275.00 (Non-members)</option>
      <option value="3">Cemerg_contactambridge ID Camp: $250.00 (members)</option>
    </select>

  </div>

  <h6 class="red-text">10% discount for early bird registrations before June 30, 2022.</h6>
  
  <small><b>I hereby release and forever discharge Roberts Canada Soccer Academy inc. its owners, authorized agents, employees and representatives from
  any liability and all causes of action, claims, damages, loss, or injuries of every nature and kind, howsoever arising, which I or the participant ever
  had, now has (have), or may hereafter have as a result of participation in this program. I authorize the provision of emergency medical services to
  the participant if deemed necessary by a qualified medical practitioner. I authorize Roberts Canada Soccer Academy Inc. to use photos or video
  excerpts of the participants, which may be used for advertising and/or instructional purposes. I certify that I am authorized to sign this release
  without the consent of any other person, as I am either the player registering and am 18 years of age or older, OR I am the parent/legal guardian of
  the player whom I am registering.</b></small>

  <center><button class="btn green">Sumbit</button></center>

     </form>
     </div>
     `
  $(document).ready(function(){
    $('.datepicker').datepicker();
  });

  $(document).ready(function(){
    $('select').formSelect();
  });

  const dataForm = document.getElementById('dataForm');
  
  dataForm.addEventListener('submit', e=>{
      e.preventDefault();
      
      let date = new Date(dataForm.dob.value);
      date = date.getFullYear() +'-'+zeroPad(date.getMonth(), 2)+'-'+zeroPad(date.getDate(), 2);

      let data = {
          name: dataForm.name.value,
          gender: dataForm.gender.value,
          date_of_birth: date,
          parent_names: dataForm.parent_names.value,
          address: dataForm.address.value,
          phone: dataForm.phone.value,
          parent_email: dataForm.parents_email.value,
          player_email: dataForm.player_email.value,
          health_card_number: dataForm.healt_card_num.value,
          medications: dataForm.medications.value,
          allergies: dataForm.allergies.value,
          injuries: dataForm.injuries.value,
          emergency_contact_number: dataForm.emerg_contact.value,
          package_guid: dataForm.reg_fees.value
      }
      if(dataForm.reg_fees.value ==="-1"){
        Swal.fire({
            icon: 'warning',
            title: 'Oops...',
            text: 'You missed to select registration fees!',
          })
      }else{
        Swal.fire({
            title: 'Do you want to submit this?',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: 'Yes',
            showDenyButton: true,
            denyButtonText: `Not yet!`,
          }).then((result) => {
            $('.load').show();
            (async () => {
              let rawResponse = null;
              let content = null;
               try{
                rawResponse = await fetch('/api/v1/campaign/create_subscriber', {
                  method: 'POST',
                  headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify(data)
                });
                content = await rawResponse.json();
              $('.load').hide();

                if(!rawResponse.ok){
                  if("error_code" in content){
                    //  console.log(content["error_code"])
                    throw Error(content["error_code"])
                    }else{
                      throw Error(rawResponse.status);
                    }
                  
                }
              } catch(err) {
               console.log(err)
               router.navigate('/error/'+err.toString())
                return;
              }
               
              // if(rawResponse){
              //   content = await rawResponse.json();
              // }
              if(content){
                  console.log(content)
                   resObj = content;
                  router.navigate('/payment');
              }else{
                Swal.fire({
                  icon: 'warning',
                  title: 'Oops...',
                  text: 'Something wrong! Re-enter Data!',
                })
              }
              })();
            if (result.isConfirmed) {
            } else if (result.isDenied) {
              Swal.fire('Not submitted!', '', 'info')
            }
          })
      }
      console.log(data);
  })



    },

    "/payment": function(){
      if(resObj===null){
        router.navigate('/');
      }else{
    
        app.innerHTML = `
        <center>
        <div class="text3x bold">ROBERTS CANADA SOCCER ACADEMY</div>
        <div class="sub2xtext">2022 Spain Id Camp Registration Form</div>
        </center>   
        <div class="form">
        <form id="payment-form">
        <h3>Payment</h3>
      <div id="payment-element">
        
      </div>
      <button id="submit">
        <div class="spinner hidden" id="spinner"></div>
        <span id="button-text">Pay now <span id="price"></span></span>
      </button>
      <div id="payment-message" class="hidden"></div>
    </form>
    </div>
        `

//Stripe
let {publishable_key, client_secret, price} = resObj;

const stripe = Stripe(publishable_key);

let elements;
let paymentElement = null;

initialize();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

async function initialize() {
  const appearance = {
    theme: 'stripe',
  };

  elements = stripe.elements();

  $('#price').text('$'+price)

   paymentElement = elements.create("card");
  paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const { error, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
    payment_method: {
      card:  paymentElement,
    }
  });

if(error){  
   router.navigate('/error/payment_error');
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occured.");
  }
} else {
  console.log(paymentIntent);
 let rawResponse = null;
 let content = null;
  (async () => {
    try{
     rawResponse = await fetch('/api/v1/campaign/post_payment_intent', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({intent: paymentIntent})
    });
    content = await rawResponse.json();
    if(!rawResponse.ok){
      
      if("error_code" in content){
        throw Error(content["error_code"])
      }else{
        throw Error(rawResponse.status);
      }
     
    }
  }catch(err){
   router.navigate('/error/'+err.toString());
   return;
  }

  //  content = await rawResponse.json();
  if(content){
     payment_res = content;
     router.navigate('/success');
  }
  })();
}
  setLoading(false);
}

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

function setLoading(isLoading) {
  if (isLoading) {
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

}
    },
    "/error/:id": function(params){
      console.log(params.id);
        app.innerHTML = `
        <center>
        <div class="text3x bold">ROBERTS CANADA SOCCER ACADEMY</div>
        <div class="sub2xtext">2022 Spain Id Camp Registration Form</div>
     </center>   
        <div class="error">
        <div style="box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em, rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset; padding: 20px; border-radius: 10px;">
        <center><img src="/assets/app/campaign/spain/images/warning.png">
        <br>
        <small>[${params.id}]</small>
        </center>
        <div class="text3x bold red-text">Oops! Process unsuccessfull! </div>
        <div style="color: crimson" class="sub2xtext">Please reload to pay again!</div>
        <br/>
        <a href="/"><center><button style="background: #F3A744;" class="btn">Reload</button></center></a>
        </div>
        </div>
        `
    },
    "success": function(){
      if(payment_res===null){
        router.navigate('/');
      }else{
        console.log(payment_res);
        app.innerHTML = `
        <center>
        <div class="text3x bold">ROBERTS CANADA SOCCER ACADEMY</div>
        <div class="sub2xtext">2022 Spain Id Camp Registration Form</div>
        </center>
        <div class="error">
        <div style="box-shadow: rgba(0, 0, 0, 0.25) 0px 0.0625em 0.0625em, rgba(0, 0, 0, 0.25) 0px 0.125em 0.5em, rgba(255, 255, 255, 0.1) 0px 0px 0px 1px inset; padding: 20px; border-radius: 10px;">
        <center><img src="/assets/app/campaign/spain/images/transaction.png"></center>
        <div class="text3x bold green-text">Hey, ${payment_res.subscriber.name}! Successfully Paid!</div>
        <div class="sub2xtext green-text">We will sent you an email with further confirmation details!</div>
        <br/>
       <center><button id="download" class="btn">Download Reciept</button></center>
        
        </div>

        <div class="reciept">
        <div class="text3xx bold">ROBERTS CANADA SOCCER ACADEMY</div>
     <div class="sub2xtext">2022 Spain Id Camp Registration</div>
     <br/>

     <div class="field"><div class="field_key">Name: </div> <div class="field_value"> ${payment_res.subscriber.name}</div></div>
     <div class="field"><div class="field_key">Gender: </div> <div class="field_value"> ${payment_res.subscriber.gender}</div></div>
     <div class="field"><div class="field_key">Date of birth: </div> <div class="field_value"> ${payment_res.subscriber.date_of_birth}</div></div>
     <div class="field"><div class="field_key">Parents' Name: </div> <div class="field_value"> ${payment_res.subscriber.parent_names}</div></div>
     <div class="field"><div class="field_key">Address: </div> <div class="field_value"> ${payment_res.subscriber.address}</div></div>
     <div class="field"><div class="field_key">Phone: </div> <div class="field_value"> ${payment_res.subscriber.phone}</div></div>
     <div class="field"><div class="field_key">Parent's Email: </div> <div class="field_value"> ${payment_res.subscriber.parent_email}</div></div>
     <div class="field"><div class="field_key">Player Email: </div> <div class="field_value"> ${payment_res.subscriber.player_email}</div></div>
     <div class="field"><div class="field_key">Health Card Number: </div> <div class="field_value"> ${payment_res.subscriber.health_card_number}</div></div>
     <div class="field"><div class="field_key">Medications: </div> <div class="field_value"> ${payment_res.subscriber.medications}</div></div>
     <div class="field"><div class="field_key">Allergies: </div> <div class="field_value"> ${payment_res.subscriber.allergies}</div></div>
     <div class="field"><div class="field_key">Injuries: </div> <div class="field_value"> ${payment_res.subscriber.injuries}</div></div>
     <div class="field"><div class="field_key">Emergency Contact: </div> <div class="field_value"> ${payment_res.subscriber.emergency_contact_number}</div></div>
     <div class="field"><div class="field_key">Campaign Name: </div> <div class="field_value"> ${payment_res.package_name}</div></div>
     <div class="field"><div class="field_key">Registration Fee: </div> <div class="field_value">$${payment_res.price}</div></div>
  <hr>
  <div class="field"><div class="field_key">Payment Transaction Id: </div> <div class="field_value">${payment_res.charge_id}</div></div>
  <div class="field"><div class="field_key">Subscriber Id: </div> <div class="field_value">${payment_res.subscriber.guid}</div></div>
  <div class="field"><div class="field_key">Package Id: </div> <div class="field_value">${payment_res.package_guid}</div></div>
   <div class="nb">I hereby release and forever discharge Roberts Canada Soccer Academy inc. its owners, authorized agents, employees and representatives from
   any liability and all causes of action, claims, damages, loss, or injuries of every nature and kind, howsoever arising, which I or the participant ever
   had, now has (have), or may hereafter have as a result of participation in this program. I authorize the provision of emergency medical services to
   the participant if deemed necessary by a qualified medical practitioner. I authorize Roberts Canada Soccer Academy Inc. to use photos or video
   excerpts of the participants, which may be used for advertising and/or instructional purposes. I certify that I am authorized to sign this release
   without the consent of any other person, as I am either the player registering and am 18 years of age or older, OR I am the parent/legal guardian of
   the player whom I am registering.</div>
        </div>
        
        </div>
        `
        $('.reciept').hide();
      const sheet = document.querySelector('.reciept')
      $('#download').click(function(){
        $('.reciept').show();
        html2pdf(sheet, {
          filename: payment_res.subscriber.name+'_'+payment_res.subscriber.guid+'.pdf',
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2 },
          jsPDF: { unit: 'pt', format: 'a4', orientation: 'portrait' }
          
      })
      $('.reciept').hide();
      })  
  }

    }
}).resolve();

const zeroPad = (num, places) => String(num).padStart(places, '0')




//transaction_guid