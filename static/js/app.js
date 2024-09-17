document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.$categories = form.querySelectorAll(".category_checkbox")

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));

            //filter institution on category change
            this.$categories.forEach(checkbox => {
                checkbox.addEventListener("change", () => {
                    const selectedCategories = Array.from(this.$categories)
                        .filter(checkbox => checkbox.checked)
                        .map(checkbox => checkbox.value);
                    this.filterInstitution(selectedCategories)
                });
            });
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // get data from inputs and show them in summary
            if (this.currentStep === 5) {
                this.$bags = document.querySelector('.bag_number').value;
                this.$institution = document.querySelector('input[name=organization]:checked');
                this.$addressInfo = document.querySelector('.address');
                this.$summary = document.querySelector('.summary')

                this.$summary.querySelector('#bags_number').innerText = this.$bags;
                this.$summary.querySelector('#selected_organization').innerText =
                    `${this.$institution.getAttribute('data-organization-type')} "${this.$institution.getAttribute('data-organization-name')}"`;
                this.$summary.querySelector('#address').innerText = this.$addressInfo.querySelector('input[name="address"]').value;
                this.$summary.querySelector('#city').innerText = this.$addressInfo.querySelector('input[name="city"]').value;
                this.$summary.querySelector('#postcode').innerText = this.$addressInfo.querySelector('input[name="postcode"]').value;
                this.$summary.querySelector('#phone_number').innerText = this.$addressInfo.querySelector('input[name="phone"]').value;
                this.$summary.querySelector('#date').innerText = this.$addressInfo.querySelector('input[name="data"]').value;
                this.$summary.querySelector('#time').innerText = this.$addressInfo.querySelector('input[name="time"]').value;
                this.$summary.querySelector('#comment').innerText = this.$addressInfo.querySelector('textarea[name="more_info"]').value;
            }
        }

        /**
         * filtering institutions
         */

        filterInstitution(selectedCategories) {

            var institutions = document.querySelectorAll('.institution');

            institutions.forEach(function (institution) {
                var categories = institution.getAttribute('data-category').split(',');

                if (selectedCategories.every(category => categories.includes(category)) || selectedCategories.length === 0) {
                    institution.style.display = 'flex';
                } else {
                    institution.style.display = 'none';
                }
            })
        }


        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            const bags = document.querySelector('input[name="bags"]').value;
            const address = document.querySelector('input[name="address"]').value;
            const city = document.querySelector('input[name="city"]').value;
            const postcode = document.querySelector('input[name="postcode"]').value;
            const phone = document.querySelector('input[name="phone"]').value;
            const date = document.querySelector('input[name="data"]').value;
            const time = document.querySelector('input[name="time"]').value;

            if (!bags || !address || !city || !postcode || !phone || !date || !time) {
                e.preventDefault();
                alert('Wszystkie pola muszą być wypełnione!');
                return;
            }
            if (isNaN(bags) || bags <= 0) {
                e.preventDefault();
                alert('Wartość torb musi być liczbą dodatnią!');
                return;
            }
            const phoneRegex = /^[+]?[0-9]{9,15}$/;
            if (!phoneRegex.test(phone)) {
                e.preventDefault();
                alert('Podaj poprawny numer telefonu!');
                return;
            }

            if (this.currentStep < 5) {
                e.preventDefault();
                this.currentStep++;
                this.updateForm();
            } else {
                console.log('Formularz przesłany');
            }
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
